from typing import List, Dict, Any
from app.models.brew import Brew


def build_brew_recommendation(brews: List[Brew]) -> Dict[str, Any]:
    if not brews:
        return {
            "session_id": None,
            "recommendation": "Log a few brews first so I can suggest a better next adjustment.",
            "suggested_changes": [],
            "summary": "No brew history yet.",
        }

    latest = brews[-1]
    previous = brews[-2] if len(brews) >= 2 else None

    suggested_changes: List[str] = []
    summary_parts: List[str] = []

    if previous is not None:
        if latest.grind_setting < previous.grind_setting:
            suggested_changes.append("Use a slightly coarser grind for the next brew.")
        elif latest.grind_setting > previous.grind_setting:
            suggested_changes.append("Use a slightly finer grind for the next brew.")

        if latest.bitterness > previous.bitterness:
            suggested_changes.append("Your last brew tasted more bitter; try a coarser grind or shorter extraction.")
        if latest.acidity > previous.acidity and latest.sweetness <= previous.sweetness:
            suggested_changes.append("Acidity increased without sweetness; try a slightly finer grind or a touch more time.")
        if latest.sweetness > previous.sweetness:
            suggested_changes.append("Sweetness improved; keep the current direction and repeat the same setup.")

        if latest.overall_score >= previous.overall_score:
            summary_parts.append("The recent trend looks positive.")
        else:
            summary_parts.append("The recent trend slipped, so a smaller adjustment may help.")

    if latest.water_temperature and latest.water_temperature >= 95:
        suggested_changes.append("Your water temperature is fairly hot; consider cooling it slightly for a cleaner cup.")
    elif latest.water_temperature and latest.water_temperature <= 90:
        suggested_changes.append("Your water temperature is on the cooler side; a slightly warmer brew may help extraction.")

    if latest.bloom_time_seconds and latest.bloom_time_seconds > 45:
        suggested_changes.append("The bloom was long; try a slightly shorter bloom next time.")
    elif latest.bloom_time_seconds and latest.bloom_time_seconds < 35:
        suggested_changes.append("The bloom was short; a little more bloom time may help development.")

    if not suggested_changes:
        suggested_changes.append("Your recent brews look balanced; keep the setup stable and focus on consistency.")

    recommendation = " ".join(suggested_changes[:3])
    summary = " ".join(summary_parts) if summary_parts else "Recent brew history reviewed."

    return {
        "session_id": None,
        "recommendation": recommendation,
        "suggested_changes": suggested_changes,
        "summary": summary,
    }
