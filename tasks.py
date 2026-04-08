import time
from typing import List, Dict, Any
from models import Ticket, SmartHomeAction, ActionType

class Task:
    def __init__(self, id: str, description: str, difficulty: str, initial_tickets: List[Ticket], expected_output: Dict[str, Any]):
        self.id = id
        self.description = description
        self.difficulty = difficulty
        self.initial_tickets = initial_tickets
        self.expected_output = expected_output

    def grade(self, history: List[SmartHomeAction], final_state: Dict[str, Any]) -> float:
        # To be implemented by subclasses
        return 0.0

class PasswordResetTask(Task):
    def grade(self, history: List[SmartHomeAction], final_state: Dict[str, Any]) -> float:
        """
        Easy task: Respond with the correct password reset link.
        """
        score = 0.0
        target_link = "https://smarthome.com/reset-password"
        for action in history:
            if action.action_type == ActionType.REPLY and action.ticket_id == "T-100":
                if action.content and target_link in action.content:
                    score = 1.0
                    break
        return score

class CameraOfflineTask(Task):
    def grade(self, history: List[SmartHomeAction], final_state: Dict[str, Any]) -> float:
        """
        Medium task: Check camera status THEN respond.
        """
        score = 0.0
        checked_camera = False
        replied_correctly = False

        for action in history:
            if action.action_type == ActionType.CHECK_DEVICE_STATUS and action.ticket_id == "T-200":
                checked_camera = True
            if action.action_type == ActionType.REPLY and action.ticket_id == "T-200" and checked_camera:
                if action.content and "offline" in action.content.lower() and "restarting" in action.content.lower():
                    replied_correctly = True
        
        if checked_camera: score += 0.4
        if replied_correctly: score += 0.6
        return min(score, 1.0)

class SecurityTriageTask(Task):
    def grade(self, history: List[SmartHomeAction], final_state: Dict[str, Any]) -> float:
        """
        Hard task: Prioritize T-301 (Security) over T-302 (Bulb).
        """
        score = 0.0
        priority_action_found = False
        correct_order = False
        
        actions_on_301 = []
        actions_on_302 = []

        for action in history:
            if action.ticket_id == "T-301":
                actions_on_301.append(action)
            elif action.ticket_id == "T-302":
                actions_on_302.append(action)
                
            if action.action_type == ActionType.PRIORITIZE_TICKET and action.ticket_id == "T-301" and action.priority == 1:
                priority_action_found = True

        # Check if T-301 was handled before T-302
        if len(actions_on_301) > 0 and (len(actions_on_302) == 0 or history.index(actions_on_301[0]) < history.index(actions_on_302[0])):
            correct_order = True

        if priority_action_found: score += 0.5
        if correct_order: score += 0.5
        return score

def get_tasks() -> Dict[str, Task]:
    now = time.time()
    return {
        "password-reset": PasswordResetTask(
            id="password-reset",
            description="Respond to a password reset request with https://smarthome.com/reset-password",
            difficulty="easy",
            initial_tickets=[
                Ticket(id="T-100", subject="Forgot Password", description="I need a link to reset my password.", created_at=now)
            ],
            expected_output={"link": "https://smarthome.com/reset-password"}
        ),
        "camera-offline": CameraOfflineTask(
            id="camera-offline",
            description="The front yard camera is offline. Check status and reply.",
            difficulty="medium",
            initial_tickets=[
                Ticket(id="T-200", subject="Camera Down", description="The camera in my yard is not showing video.", created_at=now)
            ],
            expected_output={"device": "Camera-Yard", "status": "offline"}
        ),
        "security-triage": SecurityTriageTask(
            id="security-triage",
            description="Triage these tickets. Security takes priority.",
            difficulty="hard",
            initial_tickets=[
                Ticket(id="T-301", subject="DOOR UNLOCKED", description="My front door lock just opened by itself!", created_at=now, priority=2),
                Ticket(id="T-302", subject="Bulb Color", description="I want my living room bulb to be pink.", created_at=now, priority=5)
            ],
            expected_output={"priority_ticket": "T-301"}
        )
    }
