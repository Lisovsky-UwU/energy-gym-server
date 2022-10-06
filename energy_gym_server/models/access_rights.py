class AvailableDayAccess:
    '''Права доступов для информации по дням для записи'''
    ADD = 'available day add'
    GET = 'available day get'
    DELETE = 'available day delete'

    @property
    def all_rights():
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

    @property
    def all_rights():
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

    @property
    def all_rights():
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

    @property
    def all_rights():
        return [
            *AccesRights.AVAILABLEDAY.all_rights,
            *AccesRights.STUDENT.all_rights,
            *AccesRights.ENTRY.all_rights
        ]
