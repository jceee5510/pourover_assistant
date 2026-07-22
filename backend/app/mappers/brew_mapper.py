from app.models.brew import Brew
from app.schemas.brew import BrewResponse
from app.services.brew_calculator import calculate_ratio


def brew_to_response(brew: Brew) -> BrewResponse:
    return BrewResponse(
        id=brew.id,
        dial_in_session_id=brew.dial_in_session_id,

        created_at=brew.created_at,

        dose_grams=brew.dose_grams,
        water_grams=brew.water_grams,
        water_temperature=brew.water_temperature,

        ratio=calculate_ratio(
            brew.dose_grams,
            brew.water_grams
        ),

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
    )