from sqlalchemy import Column, Integer, String

from . import Base


class Students(Base):
    __tablename__ = 'students'

    code = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    group = Column(String(20), nullable=False)
