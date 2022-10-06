class AvailableDayAccess:
    '''Права доступов для информации по дням для записи'''
    ADD = 'available day add'
    GET = 'available day get'
    DELETE = 'available day delete'


class StudentAccess:
    '''Права доступов для информации по студентам'''
    ADD = 'student add'
    GET = 'student get'
    DELETE = 'student delete'


class EntyAccess:
    '''Права доступов для информации по записям'''
    ADD = 'entry add'
    GET = 'entry get'
    DELETE = 'entry delete'


class AccesRights:
    '''Права доступов для редактирования и получения данных'''
    AVAILABLEDAY = AvailableDayAccess
    STUDENT = StudentAccess
    ENTRY = EntyAccess
