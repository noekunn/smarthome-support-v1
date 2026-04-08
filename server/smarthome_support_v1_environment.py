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
        self.done = False
        return self._get_observation()

    def step(self, action: SmartHomeAction) -> Tuple[SmartHomeObservation, float, bool, Dict[str, Any]]:
        if self.done:
            return self._get_observation(), 0.0, True, {"error": "Episode finished"}
        
        self.step_count += 1
        self.history.append(action)
        
        # Process action and calculate intermediate reward
        reward = 0.0
        result_msg = "Action completed"
        
        if action.action_type == ActionType.CLOSE_TICKET:
            self.done = True
            # Final grading
            final_score = self.current_task.grade(self.history, self.state())
            reward = final_score
        elif action.action_type == ActionType.CHECK_DEVICE_STATUS:
            status = self.device_status.get(action.ticket_id, "unknown")
            if action.ticket_id == "T-200":
                status = self.device_status.get("Camera-Yard", "unknown")
            elif action.ticket_id == "T-301":
                status = self.device_status.get("Door-Lock", "unknown")
            result_msg = f"Device status for {action.ticket_id}: {status}"
            reward = 0.05 # Small reward for information gathering
        elif action.action_type == ActionType.REPLY:
             result_msg = f"Replied to {action.ticket_id}: {action.content[:30]}..."
             reward = 0.05 # Small reward for taking action
        
        if self.step_count >= self.max_steps:
            self.done = True
            # Final grading if not already closed
            if reward < 1.0:
                 reward = self.current_task.grade(self.history, self.state())

        obs = self._get_observation()
        obs.last_action_result = result_msg
        
        return obs, reward, self.done, {}

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
