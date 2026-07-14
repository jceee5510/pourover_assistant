from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.pourover import PourOver
from app.schemas.pourover import PourOverCreate, PourOverResponse


router = APIRouter(
    prefix="/pourovers",
    tags=["pourovers"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=PourOverResponse)
def create_pourover(
    pourover: PourOverCreate,
    db: Session = Depends(get_db)
):

    new_pourover = PourOver(
        name=pourover.name,
        roaster=pourover.roaster,
        origin=pourover.origin,
        process=pourover.process,
        roast_date=pourover.roast_date,
        notes=pourover.notes
    )

    db.add(new_pourover)
    db.commit()
    db.refresh(new_pourover)

    return new_pourover

@router.get("/", response_model=list[PourOverResponse])
def get_pourovers(
    db: Session = Depends(get_db)
):
    pourovers = db.query(PourOver).all()

    return pourovers