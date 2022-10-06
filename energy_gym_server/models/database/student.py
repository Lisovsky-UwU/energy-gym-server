from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class Student(Base):
    __tablename__ = 'students'

    code = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    group = Column(String(20), nullable=False)

    entries = relationship('Entry', uselist=False, back_populates='students')
    token = relationship('Token', userlist=False, back_populates='students')
