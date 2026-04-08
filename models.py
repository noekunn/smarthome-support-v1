from enum import Enum
from typing import List, Optional, Union, Dict, Any
from pydantic import BaseModel, Field

class ActionType(str, Enum):
    REPLY = "reply"
    SEARCH_DOCS = "search_docs"
    CHECK_DEVICE_STATUS = "check_device_status"
    PRIORITIZE_TICKET = "prioritize_ticket"
    CLOSE_TICKET = "close_ticket"

class SmartHomeAction(BaseModel):
    action_type: ActionType
    ticket_id: str
    content: Optional[str] = Field(None, description="Response text or search query")
    priority: Optional[int] = Field(None, description="Priority level (1-5)")

class Ticket(BaseModel):
    id: str
    subject: str
    description: str
    status: str = "open"
    priority: int = 3
    created_at: float

class SmartHomeObservation(BaseModel):
    open_tickets: List[Ticket]
    device_status: Dict[str, str] = {}
    last_action_result: Optional[str] = None
    system_time: float

class SmartHomeReward(BaseModel):
    reward: float = Field(..., ge=-1.0, le=1.0)
    done: bool = False
    info: Dict[str, Any] = {}
