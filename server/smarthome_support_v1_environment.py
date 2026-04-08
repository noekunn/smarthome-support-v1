import time
from typing import List, Dict, Any, Tuple, Optional

try:
    from ..models import SmartHomeAction, SmartHomeObservation, SmartHomeReward, Ticket, ActionType
    from ..tasks import get_tasks
except (ImportError, ValueError):
    from models import SmartHomeAction, SmartHomeObservation, SmartHomeReward, Ticket, ActionType
    from tasks import get_tasks

class SmartHomeSupportEnv:
    def __init__(self, task_id: str = "password-reset"):
        self.task_id = task_id
        self.tasks = get_tasks()
        self.current_task = self.tasks.get(task_id, list(self.tasks.values())[0])
        self.reset()

    def reset(self) -> SmartHomeObservation:
        self.tickets = [t.model_copy() for t in self.current_task.initial_tickets]
        self.device_status = {
            "Camera-Yard": "offline",
            "Door-Lock": "unlocked",
            "Bulb-LivingRoom": "online"
        }
        self.history: List[SmartHomeAction] = []
        self.step_count = 0
        self.max_steps = 10
        self.accumulated_reward = 0.0
        self.done = False
        return self._get_observation()

    def step(self, action: SmartHomeAction) -> Tuple[SmartHomeObservation, float, bool, Dict[str, Any]]:
        if self.done:
            return self._get_observation(), 0.0, True, {"error": "Episode finished"}
        
        self.step_count += 1
        self.history.append(action)
        
        step_reward = 0.0
        result_msg = "Action completed"
        
        # Determine intermediate progress rewards and messages
        if action.action_type == ActionType.CHECK_DEVICE_STATUS:
            status = self.device_status.get(action.ticket_id, "unknown")
            if action.ticket_id == "T-200":
                status = self.device_status.get("Camera-Yard", "unknown")
            elif action.ticket_id == "T-301":
                status = self.device_status.get("Door-Lock", "unknown")
            result_msg = f"Device status for {action.ticket_id}: {status}"
            step_reward = 0.05  # Partial reward for info gathering
            
        elif action.action_type == ActionType.REPLY:
             content_snippet = action.content[:30] + "..." if action.content else "None"
             result_msg = f"Replied to {action.ticket_id}: {content_snippet}"
             step_reward = 0.05  # Partial reward for communicating

        elif action.action_type == ActionType.PRIORITIZE_TICKET:
             result_msg = f"Ticket {action.ticket_id} priority set to {action.priority}"
             step_reward = 0.05  # Partial reward for triage

        # Check for episode termination
        if action.action_type == ActionType.CLOSE_TICKET or self.step_count >= self.max_steps:
            self.done = True
            final_grade = self.current_task.grade(self.history, self.state())
            # Delta reward shaping: Ensure sum of all step rewards matches the final grade exactly
            step_reward = final_grade - self.accumulated_reward

        self.accumulated_reward += step_reward

        obs = self._get_observation()
        obs.last_action_result = result_msg
        
        return obs, step_reward, self.done, {}

    def state(self) -> Dict[str, Any]:
        return {
            "tickets": [t.dict() for t in self.tickets],
            "device_status": self.device_status,
            "step_count": self.step_count,
            "task_id": self.task_id
        }

    def _get_observation(self) -> SmartHomeObservation:
        return SmartHomeObservation(
            open_tickets=self.tickets,
            device_status=self.device_status if self.task_id != "password-reset" else {},
            system_time=time.time()
        )
