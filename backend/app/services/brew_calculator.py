def calculate_ratio(
    dose_grams: float,
    water_grams: float
):
    ratio = water_grams / dose_grams

    return f"1:{ratio:.1f}"