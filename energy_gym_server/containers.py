from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base



class DataBase(containers.DeclarativeContainer):
    config = providers.Configuration()

    engine = providers.Singleton(
        create_async_engine(
            f'postgreesql+asyncpg://{config.postgre.user}:{config.postgre.password}@{config.postgre.host}:{config.postgree.port}'
        )
    )
    Base = providers.Singleton(
        declarative_base(bind=engine)
    )


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(ini_files=["config.ini"])

    