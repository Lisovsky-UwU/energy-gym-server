class EnergyGymServerException(Exception):
    '''Базовое исключение сервера'''
    pass

class ConfigReadException(EnergyGymServerException):
    '''Исключение при чтении файла конфигурации'''
    pass