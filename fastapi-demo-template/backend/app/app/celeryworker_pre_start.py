import logging

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from fastapi_demo.db.database import get_default_bucket

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init():
    try:
        # Check Couchbase is awake
        bucket = get_default_bucket()
        logger.info(
            f"Database bucket connection established with bucket object: {bucket}"
        )
    except Exception as e:
        logger.error(e)
        raise e


def main():
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
