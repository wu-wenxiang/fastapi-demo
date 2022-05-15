from enum import Enum
from typing import List

from pydantic import BaseModel

from fastapi_demo.core.config import ROLE_SUPERUSER


class RoleEnum(Enum):
    superuser = ROLE_SUPERUSER


class Roles(BaseModel):
    roles: List[RoleEnum]
