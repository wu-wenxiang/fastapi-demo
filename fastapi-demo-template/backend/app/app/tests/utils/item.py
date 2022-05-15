from fastapi_demo import crud
from fastapi_demo.db.database import get_default_bucket
from fastapi_demo.models.item import ItemCreate
from fastapi_demo.tests.utils.user import create_random_user
from fastapi_demo.tests.utils.utils import random_lower_string


def create_random_item(owner_username: str = None):
    if owner_username is None:
        user = create_random_user()
        owner_username = user.username
    title = random_lower_string()
    description = random_lower_string()
    id = crud.utils.generate_new_id()
    item_in = ItemCreate(title=title, description=description, id=id)
    bucket = get_default_bucket()
    return crud.item.upsert(
        bucket=bucket,
        id=id,
        doc_in=item_in,
        owner_username=owner_username,
        persist_to=1,
    )
