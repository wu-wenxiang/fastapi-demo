import jwt
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from starlette.status import HTTP_403_FORBIDDEN

from fastapi_demo import crud
from fastapi_demo.core import config
from fastapi_demo.core.jwt import ALGORITHM
from fastapi_demo.db.database import get_default_bucket
from fastapi_demo.models.token import TokenPayload
from fastapi_demo.models.user import UserInDB

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/login/access-token")


def get_current_user(token: str = Security(reusable_oauth2)):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    bucket = get_default_bucket()
    user = crud.user.get(bucket, username=token_data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(current_user: UserInDB = Security(get_current_user)):
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(current_user: UserInDB = Security(get_current_user)):
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
