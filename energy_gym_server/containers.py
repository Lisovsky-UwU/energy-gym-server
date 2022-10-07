from dependency_injector import containers, providers

from .models.database import session_factory
from .config_module import Config
from .services import AvailableDaysService, UsersService, EntriesService, AuthorizationService


class Services(containers.DeclarativeContainer):
    
    config = providers.Singleton(
        Config
    )

    session_factory = providers.Callable(
        session_factory
    )

    available_day = providers.Factory(
        AvailableDaysService,
        session=session_factory
    )

    students = providers.Factory(
        UsersService,
        session=session_factory
    )

    entries = providers.Factory(
        EntriesService,
        session=session_factory
    )

    authorization = providers.Factory(
        AuthorizationService,
        session=session_factory
    )


class Application(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(packages=['.blueprints', '.services'])

    config = providers.Singleton(
        Config
    )

    services = providers.Container(
        Services,
        config = config
    )
