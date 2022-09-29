from sqlalchemy import Column, String

from . import Base


class Token(Base):
    __tablename__ = "tokens"

    token = Column(String, primary_key=True)
