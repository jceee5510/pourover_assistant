from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base


class Brew(Base):
    __tablename__ = "brews"

    id = Column(Integer, primary_key=True)

    coffee_bean_id = Column(
        Integer,
        ForeignKey("coffee_beans.id"),
        nullable=False
    )

    # Brew setup
    dose_grams = Column(Float)
    water_grams = Column(Float)
    water_temperature = Column(Float)

    grinder = Column(String)
    grind_setting = Column(Float)

    filter_paper = Column(String)
    brew_method = Column(String)

    # Timing
    bloom_time_seconds = Column(Integer)
    total_brew_time_seconds = Column(Integer)
    number_of_pours = Column(Integer)

    # Taste scores (1-10)
    sweetness = Column(Integer)
    acidity = Column(Integer)
    bitterness = Column(Integer)
    body = Column(Integer)
    clarity = Column(Integer)

    overall_score = Column(Integer)

    notes = Column(String)