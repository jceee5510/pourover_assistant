from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import SessionLocal
from app.models.brew import Brew


router = APIRouter(
    prefix="/analytics",
    tags=["analytics"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_analytics(
    db: Session = Depends(get_db)
):

    total_brews = db.query(Brew).count()

    average_score = (
        db.query(func.avg(Brew.overall_score))
        .scalar()
    )

    best_brews = (
        db.query(Brew)
        .order_by(Brew.overall_score.desc())
        .limit(5)
        .all()
    )

    return {
        "total_brews": total_brews,
        "average_score": round(average_score, 2)
            if average_score else None,
        "best_brews": [
            {
                "id": brew.id,
                "score": brew.overall_score,
                "temperature": brew.water_temperature,
                "ratio": f"1:{brew.water_grams / brew.dose_grams:.1f}",
                "grinder": brew.grinder
            }
            for brew in best_brews
        ]
    }