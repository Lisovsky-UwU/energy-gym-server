from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Token(Base):
    __tablename__ = "tokens"

    token = Column(String, primary_key=True)
    user = Column(Integer, ForeignKey('users.code'), nullable=False, index=True)

    users = relationship('User', back_populates='token')
