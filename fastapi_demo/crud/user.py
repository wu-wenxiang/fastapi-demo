import requests
from fastapi.encoders import jsonable_encoder

from fastapi_demo.core import config
from fastapi_demo.core.security import get_password_hash, verify_password
from fastapi_demo.models.config import USERPROFILE_DOC_TYPE
from fastapi_demo.models.role import RoleEnum
from fastapi_demo.models.user import UserCreate, UserInDB, UserSyncIn, UserUpdate

from . import utils

# Same as file name /app/app/search_index_definitions/users.json
full_text_index_name = "users"


def get_doc_id(username: str):
    return f"{USERPROFILE_DOC_TYPE}::{username}"


def get(*, username: str):
    doc_id = get_doc_id(username)
    return utils.get_doc(doc_id=doc_id, doc_model=UserInDB)


def get_by_email(*, email: str):
    return None
    

def insert_sync_gateway(user: UserSyncIn):
    name = user.name
    url = f"http://{config.COUCHBASE_SYNC_GATEWAY_HOST}:{config.COUCHBASE_SYNC_GATEWAY_PORT}/{config.COUCHBASE_SYNC_GATEWAY_DATABASE}/_user/{name}"
    data = jsonable_encoder(user)
    response = requests.put(url, json=data)
    return response.status_code == 200 or response.status_code == 201


def update_sync_gateway(user: UserSyncIn):
    name = user.name
    url = f"http://{config.COUCHBASE_SYNC_GATEWAY_HOST}:{config.COUCHBASE_SYNC_GATEWAY_PORT}/{config.COUCHBASE_SYNC_GATEWAY_DATABASE}/_user/{name}"
    if user.password:
        data = jsonable_encoder(user)
    else:
        data = jsonable_encoder(user, exclude={"password"})
    response = requests.put(url, json=data)
    return response.status_code == 200 or response.status_code == 201


def upsert_in_db(*, user_in: UserCreate, persist_to=0):
    user_doc_id = get_doc_id(user_in.username)
    passwordhash = get_password_hash(user_in.password)
    user = UserInDB(**user_in.dict(), hashed_password=passwordhash)
    doc_data = jsonable_encoder(user)
    return user


def update_in_db(*, username: str, user_in: UserUpdate, persist_to=0):
    user_doc_id = get_doc_id(username)
    stored_user = get(username=username)
    stored_user = stored_user.copy(update=user_in.dict(skip_defaults=True))
    if user_in.password:
        passwordhash = get_password_hash(user_in.password)
        stored_user.hashed_password = passwordhash
    data = jsonable_encoder(stored_user)
    return stored_user


def upsert(*, user_in: UserCreate, persist_to=0):
    user = upsert_in_db(user_in=user_in, persist_to=persist_to)
    user_in_sync = UserSyncIn(**user_in.dict(), name=user_in.username)
    assert insert_sync_gateway(user_in_sync)
    return user


def update(*, username: str, user_in: UserUpdate, persist_to=0):
    user = update_in_db(
        username=username, user_in=user_in, persist_to=persist_to
    )
    user_in_sync_data = user.dict()
    user_in_sync_data.update({"name": user.username})
    if user_in.password:
        user_in_sync_data.update({"password": user_in.password})
    user_in_sync = UserSyncIn(**user_in_sync_data)
    assert update_sync_gateway(user_in_sync)
    return user


def authenticate(*, username: str, password: str):
    user = get(username=username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def is_active(user: UserInDB):
    return not user.disabled


def is_superuser(user: UserInDB):
    return RoleEnum.superuser.value in utils.ensure_enums_to_strs(
        user.admin_roles or []
    )


def get_multi(*, skip=0, limit=100):
    users = utils.get_docs(
        doc_type=USERPROFILE_DOC_TYPE,
        doc_model=UserInDB,
        skip=skip,
        limit=limit,
    )
    return users


def search(*, query_string: str, skip=0, limit=100):
    users = utils.search_get_docs(
        query_string=query_string,
        index_name=full_text_index_name,
        doc_model=UserInDB,
        doc_type=USERPROFILE_DOC_TYPE,
        skip=skip,
        limit=limit,
    )
    return users


def search_get_search_results_to_docs(
    *, query_string: str, skip=0, limit=100
):
    users = utils.search_by_type_get_results_to_docs(
        query_string=query_string,
        index_name=full_text_index_name,
        doc_type=USERPROFILE_DOC_TYPE,
        doc_model=UserInDB,
        skip=skip,
        limit=limit,
    )
    return users
