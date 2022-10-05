class EnergyGymException(Exception):
    '''Базовое исключение сервера'''
    pass


class ConfigReadException(EnergyGymException):
    '''Исключение при чтении файла конфигурации'''
    pass


class DataBaseException(EnergyGymException):
    '''Исключение при работе с базой данных'''
    pass


class DataBaseConnectionException(DataBaseException):
    '''Исключение при подключении к БД'''
    pass


class AddDataCorrectException(DataBaseException):
    '''Исключение при неверных вносимныз данных в БД'''
    pass


class GetDataCorrectException(DataBaseException):
    '''Исключение при неверных данных, запрашиваемых из БД'''
    pass


class ApiException(EnergyGymException):
    '''Исключение при работе с API'''
    pass


class InvalidRequestException(ApiException):
    '''Исключение при неверном теле запроса'''
    pass
