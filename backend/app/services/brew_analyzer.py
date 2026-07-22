from app.models.brew import Brew


def analyze_brew_change(
    previous: Brew,
    current: Brew
):

    analysis = {
        "issue_detected": None,
        "adjustment_made": None,
        "result": None,
        "recommendation": None
    }


    # Grind adjustment
    if current.grind_setting < previous.grind_setting:
        analysis["adjustment_made"] = (
            "Grind was made finer."
        )

    elif current.grind_setting > previous.grind_setting:
        analysis["adjustment_made"] = (
            "Grind was made coarser."
        )


    # Overall result
    if current.overall_score > previous.overall_score:
        analysis["result"] = (
            "Brew quality improved."
        )

    elif current.overall_score < previous.overall_score:
        analysis["result"] = (
            "Brew quality declined."
        )

    else:
        analysis["result"] = (
            "Brew quality stayed the same."
        )


    # Taste changes
    bitterness_change = (
        current.bitterness - previous.bitterness
    )

    acidity_change = (
        current.acidity - previous.acidity
    )

    sweetness_change = (
        current.sweetness - previous.sweetness
    )


    if bitterness_change > 0:

        analysis["issue_detected"] = (
            "Bitterness increased."
        )

        analysis["recommendation"] = (
            "Extraction may be too high. "
            "Try a slightly coarser grind."
        )


    elif acidity_change > 0 and sweetness_change <= 0:

        analysis["issue_detected"] = (
            "Acidity increased without more sweetness."
        )

        analysis["recommendation"] = (
            "Try slightly increasing extraction "
            "with a finer grind or longer brew time."
        )


    elif sweetness_change > 0:

        analysis["issue_detected"] = (
            "Sweetness improved."
        )

        analysis["recommendation"] = (
            "This adjustment appears positive. "
            "Keep this direction."
        )


    return analysis