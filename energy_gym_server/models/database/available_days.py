from sqlalchemy import Column, Integer, Date

from . import Base


class AvailableDays(Base):
    __tablename__ = 'available_days'

    code = Column(Integer, primary_key=True, autoincrement=True)
    day = Column(Date, nullable=False)
    number_of_student = Column(Integer, nullable=False)
