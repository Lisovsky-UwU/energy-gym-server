import functools
from quart import request
from sqlalchemy.future import select
from passlib.totp import generate_secret

from .abc import BaseService
from ..models import dto, database
from ..exceptions import LoginException, TokenMissingException, IncorrectTokenException, AccessRightsException


class UserService(BaseService):

    async def generate_token(self, request: dto.LoginRequest) -> dto.TokenModel:
        db_student = await self.session.scalar(
            select(database.Student)
            .where(database.Student.name == request.username)
            .where(database.Student.password == request.password)
        )
        if db_student is None:
            raise LoginException('Неверный логин или пароль')
        
        db_token = database.Token(
            token=generate_secret(),
            user=db_student.code
        )

        self.session.add(db_token)
        await self.session.flush()

        return dto.TokenModel(
            token=db_token.token,
            user=db_token.user
        )


    @staticmethod
    def check_acces(access: str):

        def _check_auth(func):
            @functools.wraps(func)
            async def decorator(*args, **kwargs):
                request_token = request.headers.get('Authorization')
                if request_token is None:
                    raise TokenMissingException('Отсутствует заголовок Authorization')

                async with UserService() as service:
                    db_token = await service.session.get(database.Token, request_token)
                    if db_token is None:
                        raise IncorrectTokenException('Неверный токен запроса')

                    db_student = await service.session.get(database.Student, db_token.user)
                    if access not in db_student.acces_rights:
                        raise AccessRightsException('Для выполнения данной операции у вас недостаточно прав')

                return func(*args, **kwargs)

            return decorator

        return _check_auth        
