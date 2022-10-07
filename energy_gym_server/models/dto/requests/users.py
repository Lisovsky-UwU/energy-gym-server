from .. import UserModel


class RegistrationUserRequest(UserModel):
    password: str
