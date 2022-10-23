import functools
from flask import request
from sqlalchemy.future import select
from passlib.totp import generate_secret

from .abc import BaseService
from ..models import dto, database, UserRoles
from .. import exceptions


class AuthorizationService(BaseService):

    def generate_token(self, request: dto.LoginRequest) -> dto.TokenModel:
        db_user = self.session.scalar(
            select(database.User)
            .where(database.User.name == request.username)
            .where(database.User.password == request.password)
        )
        if db_user is None:
            raise exceptions.LoginException('Неверный логин или пароль')
        
        db_token = database.Token(
            token=generate_secret(),
            user=db_user.code
        )

        self.session.add(db_token)
        self.session.flush()

        return dto.TokenModel(
            token=db_token.token,
            user=db_token.user
        )


    @staticmethod
    def check_acces(access: str):

        def _check_auth(func):
            @functools.wraps(func)
            def decorator(*args, **kwargs):
                request_token = request.headers.get('Authorization')
                if request_token is None:
                    raise exceptions.TokenMissingException('Отсутствует заголовок Authorization')

                with AuthorizationService() as service:
                    db_token = service.session.get(database.Token, request_token)
                    if db_token is None:
                        raise exceptions.IncorrectTokenException('Неверный токен запроса')

                    db_user = service.session.get(database.User, db_token.user)
                    if db_user is None:
                        raise exceptions.GetDataCorrectException('Пользователь не найден')

                    if access not in UserRoles[db_user.role].value:
                        raise exceptions.AccessRightsException('Для выполнения данной операции у вас недостаточно прав')
                    
                    request.headers.add('user_code', db_user.code)

                return func(*args, **kwargs)

            return decorator

        return _check_auth
