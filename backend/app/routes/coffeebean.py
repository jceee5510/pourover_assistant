from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.coffeebean import CoffeeBean
from app.schemas.coffeebean import CoffeeBeanCreate, CoffeeBeanResponse

router = APIRouter(
    prefix="/coffee-beans",
    tags=["coffeebeans"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=CoffeeBeanResponse)
def create_coffee_beans(
    coffee_bean: CoffeeBeanCreate,
    db: Session = Depends(get_db)
):

    new_coffee_bean = CoffeeBean(
        name=coffee_bean.name,
        roaster=coffee_bean.roaster,
        origin=coffee_bean.origin,
        process=coffee_bean.process,
        roast_date=coffee_bean.roast_date,
        notes=coffee_bean.notes
    )

    db.add(new_coffee_bean)
    db.commit()
    db.refresh(new_coffee_bean)

    return new_coffee_bean

@router.get("/", response_model=list[CoffeeBeanResponse])
def get_coffee_beans(
    db: Session = Depends(get_db)
):
    coffee_beans = db.query(CoffeeBean).all()

    return coffee_beans