from pydantic import BaseModel, Field
from typing import List, Optional

class ActionItemIn(BaseModel):
    description: str
    owner: str
    due_date: Optional[str] = None

class DecisionIn(BaseModel):
    text: str

class MeetingOut(BaseModel):
    id: int
    title: str
    summary: str
    transcript: str
    action_items: List[ActionItemIn]
    decisions: List[DecisionIn]

    class Config:
        orm_mode = True
