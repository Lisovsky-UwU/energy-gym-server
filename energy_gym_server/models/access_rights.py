from typing import List


class AvailableTimeAccess:
    '''Права доступов для информации по дням для записи'''
    ADD = 'available time add'
    GET = 'available time get'
    DELETE = 'available time delete'

    def get_all_rights() -> List:
        return [
            AvailableTimeAccess.ADD,
            AvailableTimeAccess.GET,
            AvailableTimeAccess.DELETE
        ]


class UserAccess:
    '''Права доступов для информации по пользователям'''
    EDITANY = 'user edit any'
    ADD = 'user add'
    GET = 'user get'
    DELETE = 'user delete'

    def get_all_rights() -> List:
        return [
            UserAccess.EDITANY,
            UserAccess.ADD,
            UserAccess.GET,
            UserAccess.DELETE
        ]


class EntyAccess:
    '''Права доступов для информации по записям'''
    EDITANY = 'entry edit any'
    ADD = 'entry add'
    GET = 'entry get'
    DELETE = 'entry delete'

    def get_all_rights() -> List:
        return [
            EntyAccess.EDITANY,
            EntyAccess.ADD,
            EntyAccess.GET,
            EntyAccess.DELETE
        ]


class AccesRights:
    '''Права доступов для редактирования и получения данных'''
    AVAILABLETIME = AvailableTimeAccess
    USER = UserAccess
    ENTRY = EntyAccess

    def get_all_rights() -> List:
        return [
            *AccesRights.AVAILABLETIME.get_all_rights(),
            *AccesRights.USER.get_all_rights(),
            *AccesRights.ENTRY.get_all_rights()
        ]
