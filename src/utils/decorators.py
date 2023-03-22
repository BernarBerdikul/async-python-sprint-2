from functools import wraps


def coroutine(func):
    @wraps(func)
    def inner(*args, **kwargs):
        gen = func(*args, **kwargs)
        print("Generator initialization.")
        gen.send(None)
        return gen

    return inner
