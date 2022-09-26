import configparser
from pydantic import BaseModel, validator, ValidationError

from .exception import ConfigReadException


class Config(BaseModel):
    use_dev: bool
    server_port: int

    @validator('server_port')
    def validate_server_port(cls, value):
        if value not in range(0, 65536):
            raise ValidationError('Недопустимое значение порта')
        return value

try:
    config_pars = configparser.ConfigParser()
    config_pars.read('config.ini')

    config = Config(
        use_dev=config_pars['DEFAULT']['UseDev'],
        server_port=config_pars['DEFAULT']['Port']
    )
except ValidationError as e:
    raise ConfigReadException(f'Ошибка валидирования значений: {e}')
except KeyError as e:
    raise ConfigReadException(f'Ошибка чтения значения из конфига: {e}')
