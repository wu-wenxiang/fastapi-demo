from raven import Client

from fastapi_demo.core import config
from fastapi_demo.core.celery_app import celery_app

client_sentry = Client(config.SENTRY_DSN)


@celery_app.task(acks_late=True)
def test_celery(word: str):
    return f"test task return {word}"
