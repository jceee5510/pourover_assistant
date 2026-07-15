from pydantic import BaseModel


class BrewCreate(BaseModel):
    coffee_bean_id: int

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

    coffee_bean_id: int

    ratio: str
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

    class Config:
        from_attributes = True