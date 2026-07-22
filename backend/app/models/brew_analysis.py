from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class BrewAnalysis(Base):
    __tablename__ = "brew_analyses"

    id = Column(Integer, primary_key=True)

    previous_brew_id = Column(
        Integer,
        ForeignKey("brews.id"),
        nullable=False
    )

    current_brew_id = Column(
        Integer,
        ForeignKey("brews.id"),
        nullable=False
    )

    issue_detected = Column(String)

    adjustment_made = Column(String)

    result = Column(String)

    recommendation = Column(String)

    previous_brew = relationship(
        "Brew",
        foreign_keys=[previous_brew_id]
    )

    current_brew = relationship(
        "Brew",
        foreign_keys=[current_brew_id]
    )