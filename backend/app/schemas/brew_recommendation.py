from typing import List, Optional
from pydantic import BaseModel


class BrewRecommendationResponse(BaseModel):
    session_id: Optional[int] = None
    recommendation: str
    suggested_changes: List[str]
    summary: str

    class Config:
        from_attributes = True
