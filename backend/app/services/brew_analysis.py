from app.models.brew import Brew


def compare_brews(previous: Brew, current: Brew):
    observations = []

    # Grind changes
    if current.grind_setting < previous.grind_setting:
        observations.append(
            "Grind was made finer."
        )
    elif current.grind_setting > previous.grind_setting:
        observations.append(
            "Grind was made coarser."
        )

    # Water temperature
    if current.water_temperature > previous.water_temperature:
        observations.append(
            "Water temperature increased."
        )
    elif current.water_temperature < previous.water_temperature:
        observations.append(
            "Water temperature decreased."
        )

    # Overall score
    if current.overall_score > previous.overall_score:
        observations.append(
            "Overall brew quality improved."
        )
    elif current.overall_score < previous.overall_score:
        observations.append(
            "Overall brew quality declined."
        )

    return observations