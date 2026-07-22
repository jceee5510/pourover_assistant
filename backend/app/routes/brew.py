from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.brew import Brew
from app.schemas.brew import BrewCreate, BrewResponse
from app.services.brew_calculator import calculate_ratio
from app.mappers.brew_mapper import brew_to_response
from app.models.brew_analysis import BrewAnalysis
from app.services.brew_analyzer import analyze_brew_change
from fastapi import HTTPException
from app.schemas.brew_analysis import BrewAnalysisResponse

router = APIRouter(
    prefix="/brews",
    tags=["brews"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=BrewResponse)
def create_brew(
    brew: BrewCreate,
    db: Session = Depends(get_db)
):

    new_brew = Brew(
        dial_in_session_id=brew.dial_in_session_id,

        dose_grams=brew.dose_grams,
        water_grams=brew.water_grams,
        water_temperature=brew.water_temperature,

        grinder=brew.grinder,
        grind_setting=brew.grind_setting,

        filter_paper=brew.filter_paper,
        brew_method=brew.brew_method,

        bloom_time_seconds=brew.bloom_time_seconds,
        total_brew_time_seconds=brew.total_brew_time_seconds,
        number_of_pours=brew.number_of_pours,

        sweetness=brew.sweetness,
        acidity=brew.acidity,
        bitterness=brew.bitterness,
        body=brew.body,
        clarity=brew.clarity,

        overall_score=brew.overall_score,

        notes=brew.notes
    )

    db.add(new_brew)
    db.commit()
    db.refresh(new_brew)


    # Analyze previous brew in same dial-in session
    previous_brew = (
        db.query(Brew)
        .filter(
            Brew.dial_in_session_id == new_brew.dial_in_session_id,
            Brew.id != new_brew.id
        )
        .order_by(Brew.created_at.desc())
        .first()
    )


    if previous_brew:

        analysis = analyze_brew_change(
            previous_brew,
            new_brew
        )

        brew_analysis = BrewAnalysis(
            previous_brew_id=previous_brew.id,
            current_brew_id=new_brew.id,

            issue_detected=analysis["issue_detected"],
            adjustment_made=analysis["adjustment_made"],
            result=analysis["result"],
            recommendation=analysis["recommendation"]
        )

        db.add(brew_analysis)
        db.commit()   

    return brew_to_response(new_brew)


@router.get("/", response_model=list[BrewResponse])
def get_brews(
    db: Session = Depends(get_db)
):

    brews = (
        db.query(Brew)
        .order_by(Brew.created_at)
        .all()
    )   

    return [
        brew_to_response(brew)
        for brew in brews
    ]

@router.get(
    "/{brew_id}/analysis",
    response_model=BrewAnalysisResponse
)
def get_brew_analysis(
    brew_id: int,
    db: Session = Depends(get_db)
):

    analysis = (
        db.query(BrewAnalysis)
        .filter(
            BrewAnalysis.current_brew_id == brew_id
        )
        .first()
    )

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="No analysis found for this brew"
        )

    return analysis