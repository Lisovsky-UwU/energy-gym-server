from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class User(Base):
    __tablename__ = 'users'

    code = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    group = Column(String(20), nullable=False)
    password = Column(String(25), nullable=False)
    role = Column(String(15), nullable=False)

    entries = relationship('Entry', uselist=False, back_populates='users')
    token = relationship('Token', uselist=False, back_populates='users')
