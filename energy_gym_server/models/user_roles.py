from enum import Enum

from .access_rights import AccesRights


class UserRoles(Enum):
    
    STUDENT = [
        AccesRights.AVAILABLEDAY.GET,
        AccesRights.ENTRY.ADD,
        AccesRights.ENTRY.GET
    ]

    ADMIN = [
        AccesRights.all_rights
    ]
