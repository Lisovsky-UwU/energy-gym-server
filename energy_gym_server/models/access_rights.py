from typing import List


class AvailableDayAccess:
    '''Права доступов для информации по дням для записи'''
    ADD = 'available day add'
    GET = 'available day get'
    DELETE = 'available day delete'

    def get_all_rights() -> List:
        return [
            AvailableDayAccess.ADD,
            AvailableDayAccess.GET,
            AvailableDayAccess.DELETE
        ]


class StudentAccess:
    '''Права доступов для информации по студентам'''
    EDITANY = 'student edit any'
    ADD = 'student add'
    GET = 'student get'
    DELETE = 'student delete'

    def get_all_rights() -> List:
        return [
            StudentAccess.EDITANY,
            StudentAccess.ADD,
            StudentAccess.GET,
            StudentAccess.DELETE
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
    AVAILABLEDAY = AvailableDayAccess
    STUDENT = StudentAccess
    ENTRY = EntyAccess

    def get_all_rights() -> List:
        return [
            *AccesRights.AVAILABLEDAY.get_all_rights(),
            *AccesRights.STUDENT.get_all_rights(),
            *AccesRights.ENTRY.get_all_rights()
        ]
