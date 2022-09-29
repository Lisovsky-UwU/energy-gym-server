class EnergyGymException(Exception):
    '''Базовое исключение сервера'''
    pass


class DataBaseException(EnergyGymException):
    '''Исключение при работе с базой данных'''
    pass

class DataBaseConnectionException(DataBaseException):
    '''Исключение при подключении к БД'''
    pass
