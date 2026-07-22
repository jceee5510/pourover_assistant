from pydantic import BaseModel
from datetime import datetime


class BrewCreate(BaseModel):

    dial_in_session_id: int

    dose_grams: float
    water_grams: float
    water_temperature: float

    grinder: str
    grind_setting: float

    filter_paper: str
    brew_method: str

    bloom_time_seconds: int
    total_brew_time_seconds: int
    number_of_pours: int

    sweetness: int
    acidity: int
    bitterness: int
    body: int
    clarity: int

    overall_score: int

    notes: str


class BrewResponse(BaseModel):
    id: int

    dial_in_session_id: int

    created_at: datetime

    dose_grams: float
    water_grams: float
    water_temperature: float

    ratio: str

    grinder: str
    grind_setting: float

    filter_paper: str
    brew_method: str

    bloom_time_seconds: int
    total_brew_time_seconds: int
    number_of_pours: int

    sweetness: int
    acidity: int
    bitterness: int
    body: int
    clarity: int

    overall_score: int

    notes: str

    class Config:
        from_attributes = True