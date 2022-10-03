from sqlalchemy.orm import Session

from ..exceptions import DataBaseConnectionException


class DataBaseService:
    
    def __init__(self, session: Session):
        self.session = session

    def __getattr__(self, attr):
        return getattr(self.session, attr)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

        if exc_type is not None:
            if issubclass(exc_type, ConnectionError):
                raise DataBaseConnectionException("Отсутствует соединение с базой данных")


from .available_days import AvailableDaysService
from .students import StudentsService
from .entries import EntriesService
