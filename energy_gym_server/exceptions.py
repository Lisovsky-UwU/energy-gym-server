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


class TokenMissingException(ApiException):
    '''Исключение из-за отсутствия токена в заголовке запроса'''
    pass


class IncorrectTokenException(ApiException):
    '''Исключение при неверном токене'''
    pass


class AccessRightsException(ApiException):
    '''Исключение при отсутствии необходимых прав'''
    pass


class InvalidRequestException(ApiException):
    '''Исключение при неверном теле запроса'''
    pass


class LoginException(EnergyGymException):
    '''Исключение при ошибке входа'''
    pass
