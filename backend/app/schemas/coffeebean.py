from datetime import date
from pydantic import BaseModel


class CoffeeBeanCreate(BaseModel):
    name: str
    roaster: str
    origin: str
    process: str
    roast_date: date
    notes: str


class CoffeeBeanResponse(BaseModel):
    id: int
    name: str
    roaster: str
    origin: str
    process: str
    roast_date: date
    notes: str

    class Config:
        from_attributes = True

