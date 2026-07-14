from sqlalchemy import Column, Integer, String, Date
from app.database import Base


class PourOver(Base):
    __tablename__ = "pourovers"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    roaster = Column(String)

    origin = Column(String)

    process = Column(String)

    roast_date = Column(Date)

    notes = Column(String)