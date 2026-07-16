from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.brew import BrewResponse
from typing import List

class DialInSessionCreate(BaseModel):
    coffee_bean_id: int

    goal_type: str
    desired_notes: str
    preferred_profile: str


class DialInSessionUpdate(BaseModel):
    status: Optional[str] = None
    goal_type: Optional[str] = None
    desired_notes: Optional[str] = None
    preferred_profile: Optional[str] = None
    completed_at: Optional[datetime] = None


class DialInSessionResponse(BaseModel):
    id: int

    coffee_bean_id: int

    status: str
    goal_type: Optional[str] = None
    desired_notes: Optional[str] = None
    preferred_profile: Optional[str] = None

    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class DialInSessionDetailResponse(BaseModel):
    id: int

    coffee_bean_id: int

    status: str
    goal_type: Optional[str] = None
    desired_notes: Optional[str] = None
    preferred_profile: Optional[str] = None

    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    brews: List[BrewResponse]

    class Config:
        from_attributes = True