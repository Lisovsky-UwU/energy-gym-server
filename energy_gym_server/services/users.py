from sqlalchemy.future import select
from sqlalchemy.sql import any_
from flask import request as flask_request

from .abc import BaseService
from ..models import dto, database, AccesRights, UserRoles
from ..exceptions import AddDataCorrectException, GetDataCorrectException, AccessRightsException


class UsersService(BaseService):

    def get_user_list(self) -> dto.UserList:
        return dto.UserList(
            user_list=[
                dto.UserModel(
                    code=db_user.code,
                    name=db_user.name,
                    group=db_user.group
                )
                for db_user in (
                    self.session.scalars(select(database.User))
                )
            ]
        )
    

    def get_by_code(self, request: dto.ItemByCodeRequest) -> dto.UserModel:
        self.__check_access_for_user__(int(flask_request.headers.get('user_code')), request.code)

        user = self.session.get(database.User, request.code)
        if user is None:
            raise GetDataCorrectException('Пользователь с запрашиваемым кодом не найден')

        return dto.UserModel(
            code=user.code,
            name=user.name,
            group=user.group
        )


    def add_user(self, request: dto.RegistrationUserRequest) -> dto.UserModel:
        if self.session.get(database.User, request.code) is not None:
            raise AddDataCorrectException('Пользователь с данным идентефикатором уже существует')

        user = database.User(
            **request.dict(),
            role=UserRoles.STUDENT.name
        )
        self.session.add(user)
        self.session.flush()

        return dto.UserModel(
            code=user.code,
            name=user.name,
            group=user.group
        )


    def delete_user(self, request: dto.ItemDeleteRequest) -> dto.ItemsDeleted:
        self.__check_access_for_user__(int(flask_request.headers.get('user_code')), request.code)

        for db_entry in (
            self.session.scalars(
                select(database.Entry)
                .where(database.Entry.user == request.code)
            )
        ):
            self.session.delete(db_entry)

        for db_token in (
            self.session.scalars(
                select(database.Token)
                .where(database.Token.user == request.code)
            )
        ):
            self.session.delete(db_token)

        self.session.delete(
            self.session.get(database.User, request.code)
        )

        return dto.ItemsDeleted(
            result_text='Студент успешно удален'
        )


    def __check_access_for_user__(self, user_code: int, access_user_code: int):
        db_user: database.User = self.session.get(database.User, user_code)

        if AccesRights.USER.EDITANY not in UserRoles[db_user.role].value and db_user.code != access_user_code:
            raise AccessRightsException('Для выполнения данной операции у вас недостаточно прав')
