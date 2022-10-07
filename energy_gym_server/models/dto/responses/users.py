from typing import List
from pydantic import BaseModel

from .. import UserModel


class UserList(BaseModel):
    user_list: List[UserModel]
