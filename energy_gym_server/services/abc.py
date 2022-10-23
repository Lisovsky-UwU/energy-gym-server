import asyncio
from sqlalchemy.orm import Session

from ..exceptions import DataBaseConnectionException
from ..models.database import session_factory


class BaseService:
    
    def __init__(self, session: Session = None, **kwargs):
        if session is None:
            self.session = session_factory(**kwargs)
        else:
            self.session = session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

        if exc_type is not None:
            if issubclass(exc_type, ConnectionError):
                raise DataBaseConnectionException("Отсутствует соединение с базой данных")

    def commit(self):
        self.session.commit()

    def close(self):
        self.session.close()
