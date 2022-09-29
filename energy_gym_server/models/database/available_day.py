from email.policy import default
from sqlalchemy import Column, Integer, Date
from sqlalchemy.orm import relationship

from . import Base


class AvailableDay(Base):
    __tablename__ = 'available_days'

    code = Column(Integer, primary_key=True, autoincrement=True)
    day = Column(Date, nullable=False)
    number_of_students = Column(Integer, nullable=False)

    entries = relationship('Entry', uselist=False, back_populates='available_days')
