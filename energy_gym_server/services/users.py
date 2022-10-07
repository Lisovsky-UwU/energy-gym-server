from sqlalchemy.future import select
from sqlalchemy.sql import any_
from quart import request as quart_request

from .abc import AsyncBaseService
from ..models import dto, database, AccesRights, UserRoles
from ..exceptions import AddDataCorrectException, GetDataCorrectException, AccessRightsException


class UsersService(AsyncBaseService):

    async def get_user_list(self) -> dto.UserList:
        return dto.UserList(
            user_list=[
                dto.UserModel(
                    code=db_user.code,
                    name=db_user.name,
                    group=db_user.group
                )
                for db_user in (
                    await self.session.scalars(select(database.User))
                )
            ]
        )
    

    async def get_by_code(self, request: dto.ItemByCodeRequest) -> dto.UserModel:
        await self.__check_access_for_user__(int(quart_request.headers.get('user_code')), request.code)

        user = await self.session.get(database.User, request.code)
        if user is None:
            raise GetDataCorrectException('Пользователь с запрашиваемым кодом не найден')

        return dto.UserModel(
            code=user.code,
            name=user.name,
            group=user.group
        )


    async def get_list_by_codes(self, request: dto.ItemListByCodesRequest) -> dto.UserList:
        return dto.UserList(
            user_list=[
                dto.UserModel(
                    code=db_user.code,
                    name=db_user.name,
                    group=db_user.group
                )
                for db_user in (
                    await self.session.scalars(
                        select(database.User)
                        .where(database.User.code == any_(request.code_list))
                    )
                )
            ]
        )


    async def add_user(self, request: dto.RegistrationUserRequest) -> dto.UserModel:
        if await self.session.get(database.User, request.code) is not None:
            raise AddDataCorrectException('Пользователь с данным идентефикатором уже существует')

        user = database.User(
            **request.dict(),
            role=UserRoles.STUDENT.name
        )
        self.session.add(user)
        await self.session.flush()

        return dto.UserModel(
            code=user.code,
            name=user.name,
            group=user.group
        )


    async def delete_user(self, request: dto.ItemDeleteRequest) -> dto.ItemsDeleted:
        await self.__check_access_for_user__(int(quart_request.headers.get('user_code')), request.code)

        for db_entry in (
            await self.session.scalars(
                select(database.Entry)
                .where(database.Entry.user == request.code)
            )
        ):
            await self.session.delete(db_entry)

        for db_token in (
            await self.session.scalars(
                select(database.Token)
                .where(database.Token.user == request.code)
            )
        ):
            await self.session.delete(db_token)

        await self.session.delete(
            await self.session.get(database.User, request.code)
        )

        return dto.ItemsDeleted(
            result_text='Студент успешно удален'
        )


    async def __check_access_for_user__(self, user_code: int, access_user_code: int):
        db_user: database.User = await self.session.get(database.User, user_code)

        if AccesRights.STUDENT.EDITANY not in UserRoles[db_user.role].value and db_user.code != access_user_code:
            raise AccessRightsException('Для выполнения данной операции у вас недостаточно прав')
