from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.brew import Brew
from app.schemas.brew import BrewCreate, BrewResponse
from app.services.brew_calculator import calculate_ratio


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
        coffee_bean_id=brew.coffee_bean_id,

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

    response = BrewResponse(
        id=new_brew.id,
        coffee_bean_id=new_brew.coffee_bean_id,

        dose_grams=new_brew.dose_grams,
        water_grams=new_brew.water_grams,
        water_temperature=new_brew.water_temperature,

        grinder=new_brew.grinder,
        grind_setting=new_brew.grind_setting,

        filter_paper=new_brew.filter_paper,
        brew_method=new_brew.brew_method,

        bloom_time_seconds=new_brew.bloom_time_seconds,
        total_brew_time_seconds=new_brew.total_brew_time_seconds,
        number_of_pours=new_brew.number_of_pours,

        sweetness=new_brew.sweetness,
        acidity=new_brew.acidity,
        bitterness=new_brew.bitterness,
        body=new_brew.body,
        clarity=new_brew.clarity,

        overall_score=new_brew.overall_score,

        notes=new_brew.notes,

        ratio=calculate_ratio(
            new_brew.dose_grams,
            new_brew.water_grams
        )
    )

    return response


@router.get("/", response_model=list[BrewResponse])
def get_brews(
    db: Session = Depends(get_db)
):

    brews = db.query(Brew).all()

    responses = []

    for brew in brews:

        response = BrewResponse(
            id=brew.id,
            coffee_bean_id=brew.coffee_bean_id,

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

            notes=brew.notes,

            ratio=calculate_ratio(
                brew.dose_grams,
                brew.water_grams
            )
        )

        responses.append(response)

    return responses