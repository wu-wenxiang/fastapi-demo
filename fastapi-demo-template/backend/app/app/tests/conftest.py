import pytest

from fastapi_demo.core import config
from fastapi_demo.tests.utils.utils import get_server_api, get_superuser_token_headers
from fastapi_demo.tests.utils.user import authentication_token_from_email


@pytest.fixture(scope="module")
def server_api():
    return get_server_api()


@pytest.fixture(scope="module")
def superuser_token_headers():
    return get_superuser_token_headers()


@pytest.fixture(scope="module")
def normal_user_token_headers():
    return authentication_token_from_email(config.EMAIL_TEST_USER)
