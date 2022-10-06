from sqlalchemy import Column, String, Integer, ForeignKey, ARRAY
from sqlalchemy.orm import relationship

from . import Base


class Token(Base):
    __tablename__ = "tokens"

    token = Column(String, primary_key=True)
    user = Column(Integer, ForeignKey('students.code'), nullable=False, index=True)
    acces_rights = Column(ARRAY(String), nullable=False)

    students = relationship('Student', back_populates='token')
