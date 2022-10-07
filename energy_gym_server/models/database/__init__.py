from asyncio import current_task
from sqlalchemy.ext.asyncio import create_async_engine, async_scoped_session, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ...config_module import config


engine = create_async_engine(config.postgre.connect_str, future=True)
Base = declarative_base(bind=engine)


def session_factory(**kwargs):
    return async_scoped_session(
        sessionmaker(
            bind=engine,
            autocommit=False,
            autoflush=False,
            class_=AsyncSession,
            future=True,
            **kwargs
        ),
        scopefunc=current_task
    )


from .available_day import AvailableDay
from .entry import Entry
from .user import User
from .token import Token