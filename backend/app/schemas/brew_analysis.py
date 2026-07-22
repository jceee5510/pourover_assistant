from typing import Optional

from pydantic import BaseModel


class BrewAnalysisResponse(BaseModel):
    id: int

    previous_brew_id: int
    current_brew_id: int

    issue_detected: Optional[str] = None
    adjustment_made: Optional[str] = None
    result: Optional[str] = None
    recommendation: Optional[str] = None

    class Config:
        from_attributes = True