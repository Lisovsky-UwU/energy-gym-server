from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class RegistrationUserRequest(UserModel):
    password: str
