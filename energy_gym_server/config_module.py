import configparser
from pydantic import BaseModel, validator, ValidationError

from .exceptions import ConfigReadException


def validate_port(value: int) -> int:
    if value not in range(0, 65536):
        raise ValidationError('Недопустимое значение порта')
    return value


class Default(BaseModel):
    use_dev: bool
    server_port: int

    # validators
    _validate_port = validator('server_port', allow_reuse=True)(validate_port)


class Postgre(BaseModel):
    host: str
    port: int
    database: str
    user: str
    password: str

    @property
    def connect_str(self):
        return f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}'

    # validators
    _validate_port = validator('port', allow_reuse=True)(validate_port)


class Config(BaseModel):
    default: Default
    postgre: Postgre


try:
    config_pars = configparser.ConfigParser()
    config_pars.read('config.ini')

    config = Config(
        default = Default(**config_pars['DEFAULT']),
        postgre = Postgre(**config_pars['postgre'])
    )
except ValidationError as e:
    raise ConfigReadException(f'Ошибка валидирования значений: {e}')
except KeyError as e:
    raise ConfigReadException(f'Ошибка чтения значения из конфига: {e}')
