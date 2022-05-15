from fastapi_demo.core import config
from fastapi_demo.models.config import ITEM_DOC_TYPE
from fastapi_demo.models.item import ItemCreate, ItemInDB, ItemUpdate

from . import utils

# Same as file name /app/app/search_index_definitions/items.json
full_text_index_name = "items"


def get_doc_id(id: str):
    return f"{ITEM_DOC_TYPE}::{id}"


def get(*, id: str):
    doc_id = get_doc_id(id)
    return utils.get_doc(doc_id=doc_id, doc_model=ItemInDB)


def upsert(
    *,
    id: str,
    doc_in: ItemCreate,
    owner_username: str,
    persist_to=0,
    ttl=0,
):
    doc_id = get_doc_id(id)
    doc = ItemInDB(**doc_in.dict(), id=id, owner_username=owner_username)
    return utils.upsert(
        doc_id=doc_id, doc_in=doc, persist_to=persist_to, ttl=ttl
    )


def update(
    *,
    id: str,
    doc_in: ItemUpdate,
    owner_username=None,
    persist_to=0,
    ttl=0,
):
    doc_id = get_doc_id(id=id)
    doc = get(id=id)
    doc = doc.copy(update=doc_in.dict(skip_defaults=True))
    if owner_username is not None:
        doc.owner_username = owner_username
    return utils.upsert(
        doc_id=doc_id, doc_in=doc, persist_to=persist_to, ttl=ttl
    )


def remove(*, id: str, persist_to=0):
    doc_id = get_doc_id(id)
    return utils.remove(
        doc_id=doc_id, doc_model=ItemInDB, persist_to=persist_to
    )


def get_multi(*, skip=0, limit=100):
    return utils.get_docs(
        doc_type=ITEM_DOC_TYPE,
        doc_model=ItemInDB,
        skip=skip,
        limit=limit,
    )


def get_multi_by_owner(*, owner_username: str, skip=0, limit=100):
    return None


def search(*, query_string: str, skip=0, limit=100):
    docs = utils.search_get_docs(
        query_string=query_string,
        index_name=full_text_index_name,
        doc_model=ItemInDB,
        skip=skip,
        limit=limit,
    )
    return docs


def search_with_owner(
    *query_string: str, username: str, skip=0, limit=100
):
    username_filter = f"owner_username:{username}"
    if username_filter not in query_string:
        query_string = f"{query_string} {username_filter}"
    docs = utils.search_get_docs(
        query_string=query_string,
        index_name=full_text_index_name,
        doc_model=ItemInDB,
        skip=skip,
        limit=limit,
    )
    return docs


def search_get_search_results_to_docs(
    *, query_string: str, skip=0, limit=100
):
    docs = utils.search_by_type_get_results_to_docs(
        query_string=query_string,
        index_name=full_text_index_name,
        doc_type=ITEM_DOC_TYPE,
        doc_model=ItemInDB,
        skip=skip,
        limit=limit,
    )
    return docs
