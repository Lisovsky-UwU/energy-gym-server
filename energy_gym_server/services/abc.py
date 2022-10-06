import asyncio
from sqlalchemy.orm import Session

from ..exceptions import DataBaseConnectionException
from ..models.database import session_factory


class AsyncBaseService:
    
    def __init__(self, session: Session = None, **kwargs):
        if session is None:
            self.session = session_factory(**kwargs)
        else:
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
