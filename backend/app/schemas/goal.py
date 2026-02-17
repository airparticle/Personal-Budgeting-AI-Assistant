from pydantic import BaseModel
from typing import Optional


class GoalBase(BaseModel):
    goal_name: str
    target_value: float
    current_progress: float = 0.0


class GoalCreate(GoalBase):
    pass


class GoalUpdate(BaseModel):
    goal_name: Optional[str] = None
    target_value: Optional[float] = None
    current_progress: Optional[float] = None


class GoalResponse(GoalBase):
    goal_id: int
    user_id: int

    class Config:
        from_attributes = True