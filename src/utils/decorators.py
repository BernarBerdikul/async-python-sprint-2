import logging
from functools import wraps

logger = logging.getLogger(__name__)


def coroutine(func):
    @wraps(func)
    def inner(*args, **kwargs):
        gen = func(*args, **kwargs)
        logger.debug("Generator initialization.")
        gen.send(None)
        return gen

    return inner
