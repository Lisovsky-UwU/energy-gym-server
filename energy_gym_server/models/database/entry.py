from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Entry(Base):
    __tablename__ = 'entries'

    code = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(DateTime, nullable=False)
    selected_day = Column(Integer, ForeignKey('available_days.code'), nullable=False, index=True)
    user = Column(Integer, ForeignKey('users.code'), nullable=False, index=True)

    available_days = relationship('AvailableDay', back_populates='entries')
    users = relationship('User', back_populates='entries')
