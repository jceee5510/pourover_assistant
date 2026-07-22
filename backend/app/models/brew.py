from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from app.database import Base
from sqlalchemy.orm import relationship
from app.services.brew_calculator import calculate_ratio
from datetime import datetime

class Brew(Base):
    __tablename__ = "brews"

    id = Column(Integer, primary_key=True)

    dial_in_session_id = Column(
        Integer,
        ForeignKey("dial_in_sessions.id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
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

    dial_in_session = relationship(
        "DialInSession",
        back_populates="brews"
    )

    @property
    def ratio(self):
        return calculate_ratio(
            self.dose_grams,
            self.water_grams
        )

    previous_analyses = relationship(
        "BrewAnalysis",
        foreign_keys="BrewAnalysis.previous_brew_id"
    )

    next_analyses = relationship(
        "BrewAnalysis",
        foreign_keys="BrewAnalysis.current_brew_id"
    )