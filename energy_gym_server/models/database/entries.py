from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Entries(Base):
    __tablename__ = 'entries'

    code = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(DateTime, nullable=False)
    selected_day = Column(Integer, ForeignKey('available_days.code'), nullable=False, index=True)
    student = Column(Integer, ForeignKey('students.code'), nullable=False, index=True)

    available_days = relationship('AvailableDays')
    students = relationship('Students')
