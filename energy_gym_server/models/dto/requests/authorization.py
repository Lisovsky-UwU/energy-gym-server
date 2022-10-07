from pydantic import BaseModel

from ..common import UserModel


class LoginRequest(BaseModel):
    username: str
    password: str


class RegistrationUserRequest(UserModel):
    password: str
