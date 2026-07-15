from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.database import Base


class CoffeeBean(Base):
    __tablename__ = "coffee_beans"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    roaster = Column(String)

    origin = Column(String)

    process = Column(String)

    roast_date = Column(Date)

    notes = Column(String)

    brews = relationship(
        "Brew",
        backref="coffee_bean"
    )