from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class DialInSession(Base):
    __tablename__ = "dial_in_sessions"

    id = Column(Integer, primary_key=True)

    coffee_bean_id = Column(
        Integer,
        ForeignKey("coffee_beans.id"),
        nullable=False
    )

    status = Column(
        String,
        default="ACTIVE"
    )

    goal_type = Column(String)

    desired_notes = Column(String)

    preferred_profile = Column(String)

    started_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    completed_at = Column(
        DateTime,
        nullable=True
    )

    coffee_bean = relationship(
        "CoffeeBean",
        back_populates="dial_in_sessions"
    )

    brews = relationship(
        "Brew",
        back_populates="dial_in_session"
    )