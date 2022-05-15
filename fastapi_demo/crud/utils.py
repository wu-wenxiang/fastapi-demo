import uuid
from enum import Enum
from typing import List, Optional, Sequence, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pydantic.fields import Field, SHAPE_LIST, SHAPE_SET, SHAPE_TUPLE

from fastapi_demo.core import config

PydanticModel = TypeVar("PydanticModel", bound=BaseModel)


def generate_new_id():
    return str(uuid.uuid4())


def ensure_enums_to_strs(items: Union[Sequence[Union[Enum, str]], Type[Enum]]):
    str_items = []
    for item in items:
        if isinstance(item, Enum):
            str_items.append(str(item.value))
        else:
            str_items.append(str(item))
    return str_items


def get_doc_results_by_type(*, doc_type: str, skip=0, limit=100):
    return None


def get_docs_by_keys(
    *, keys: List[str], doc_model=Type[PydanticModel]
) -> List[PydanticModel]:
    return []


def doc_result_to_model(
    couchbase_result, *, doc_model: Type[PydanticModel]
) -> PydanticModel:
    data = couchbase_result[config.COUCHBASE_BUCKET_NAME]
    doc = doc_model(**data)
    return doc


def doc_results_to_model(
    results_from_couchbase: list, *, doc_model: Type[PydanticModel]
) -> List[PydanticModel]:
    items = []
    for doc in results_from_couchbase:
        data = doc[config.COUCHBASE_BUCKET_NAME]
        doc = doc_model(**data)
        items.append(doc)
    return items


def search_results_to_model(
    results_from_couchbase: list, *, doc_model: Type[PydanticModel]
) -> List[PydanticModel]:
    items = []
    for doc in results_from_couchbase:
        data = doc.get("fields")
        if not data:
            continue
        data_nones = {}
        for key, value in data.items():
            field: Field = doc_model.__fields__[key]
            if not value:
                value = None
            elif field.shape in {SHAPE_LIST, SHAPE_SET, SHAPE_TUPLE} and not isinstance(
                value, list
            ):
                value = [value]
            data_nones[key] = value
        doc = doc_model(**data_nones)
        items.append(doc)
    return items


def get_docs(
    *, doc_type: str, doc_model=Type[PydanticModel], skip=0, limit=100
) -> List[PydanticModel]:
    doc_results = get_doc_results_by_type(
        doc_type=doc_type, skip=skip, limit=limit
    )
    return doc_results_to_model(doc_results, doc_model=doc_model)


def get_doc(
    *, doc_id: str, doc_model: Type[PydanticModel]
) -> Optional[PydanticModel]:
    return None


def upsert(
    *, doc_id: str, doc_in: PydanticModel, persist_to=0, ttl=0
) -> Optional[PydanticModel]:
    doc_data = jsonable_encoder(doc_in)
    return None


def update(
    *,
    doc_id: str,
    doc: PydanticModel,
    doc_updated: PydanticModel,
    persist_to=0,
    ttl=0,
):
    doc_updated = doc.copy(update=doc_updated.dict(skip_defaults=True))
    data = jsonable_encoder(doc_updated)
    return doc_updated


def remove(
    *, doc_id: str, doc_model: Type[PydanticModel] = None, persist_to=0
) -> Optional[Union[PydanticModel, bool]]:
    return None


def search_get_doc_ids(
    *,
    query_string: str,
    index_name: str,
    skip: int = 0,
    limit: int = 100,
) -> List[str]:
    doc_ids = []
    return doc_ids


def search_get_search_results(
    *,
    query_string: str,
    index_name: str,
    skip: int = 0,
    limit: int = 100,
):
    docs = []
    return docs


def search_by_type_get_search_results(
    *,
    query_string: str,
    index_name: str,
    doc_type: str,
    skip: int = 0,
    limit: int = 100,
):
    type_filter = f"type:{doc_type}"
    if not query_string:
        query_string = type_filter
    if query_string and type_filter not in query_string:
        query_string += f" {type_filter}"
    docs = []
    return docs


def search_get_docs(
    *,
    query_string: str,
    index_name: str,
    doc_model: Type[PydanticModel],
    doc_type: str = None,
    skip=0,
    limit=100,
) -> List[PydanticModel]:
    if doc_type is not None:
        type_filter = f"type:{doc_type}"
        if not query_string:
            query_string = type_filter
        if query_string and type_filter not in query_string:
            query_string += f" {type_filter}"
    keys = search_get_doc_ids(
        query_string=query_string,
        index_name=index_name,
        skip=skip,
        limit=limit,
    )
    if not keys:
        return []
    return get_docs_by_keys(keys=keys, doc_model=doc_model)


def search_get_search_results_to_docs(
    *,
    query_string: str,
    index_name: str,
    doc_model: Type[PydanticModel],
    skip=0,
    limit=100,
) -> List[PydanticModel]:
    doc_results = search_get_search_results(
        query_string=query_string,
        index_name=index_name,
        skip=skip,
        limit=limit,
    )
    return search_results_to_model(doc_results, doc_model=doc_model)


def search_by_type_get_results_to_docs(
    *,
    query_string: str,
    index_name: str,
    doc_type: str,
    doc_model: Type[PydanticModel],
    skip=0,
    limit=100,
) -> List[PydanticModel]:
    doc_results = search_by_type_get_search_results(
        query_string=query_string,
        index_name=index_name,
        doc_type=doc_type,
        skip=skip,
        limit=limit,
    )
    return search_results_to_model(doc_results, doc_model=doc_model)
