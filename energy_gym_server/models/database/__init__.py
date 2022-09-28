from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from ...config_module import config


engine = create_async_engine(config.postgre.connect_str, future=True)
Base = declarative_base(bind=engine)
