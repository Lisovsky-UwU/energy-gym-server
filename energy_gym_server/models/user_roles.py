from enum import Enum

from .access_rights import AccesRights


class UserRoles(Enum):
    
    STUDENT = [
        AccesRights.AVAILABLEDAY.GET,
        AccesRights.ENTRY.ADD,
        AccesRights.ENTRY.GET,
        AccesRights.USER.GET,
        AccesRights.USER.DELETE
    ]

    ADMIN = [
        *AccesRights.get_all_rights()
    ]
