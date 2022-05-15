from fastapi_demo.core.config import (
    COUCHBASE_BUCKET_NAME,
    COUCHBASE_HOST,
    COUCHBASE_N1QL_TIMEOUT_SECS,
    COUCHBASE_OPERATION_TIMEOUT_SECS,
    COUCHBASE_PASSWORD,
    COUCHBASE_PORT,
    COUCHBASE_USER,
)
from fastapi_demo.db.couchbase_utils import get_cluster_couchbase_url


def get_default_bucket():
    return get_bucket(
        COUCHBASE_USER,
        COUCHBASE_PASSWORD,
        COUCHBASE_BUCKET_NAME,
        host=COUCHBASE_HOST,
        port=COUCHBASE_PORT,
    )


def get_cluster(username: str, password: str, host="couchbase", port="8091"):
    # cluster_url="couchbase://couchbase"
    # username = "Administrator"
    # password = "password"
    cluster_url = get_cluster_couchbase_url(host=host, port=port)
    return None


def get_bucket(
    username: str,
    password: str,
    bucket_name: str,
    host="couchbase",
    port="8091",
    timeout: float = COUCHBASE_OPERATION_TIMEOUT_SECS,
    n1ql_timeout: float = COUCHBASE_N1QL_TIMEOUT_SECS,
):
    cluster = get_cluster(username, password, host=host, port=port)
    return None


def ensure_create_primary_index():
    return None


def ensure_create_type_index():
    return None
