from typing import Generator

from src.clients.weather_api import get_city_weather
from src.utils.decorators import coroutine


def say_hello(name: str):
    return f"Hello {name}!"


@coroutine
def task_with_network():
    while True:
        try:
            # Get sent data from coroutine
            city_name = yield
            yield get_city_weather(city_name)
        except GeneratorExit:
            print("Выход из корутины")
            raise


if __name__ == "__main__":
    coro: Generator = task_with_network()
    cities = ["MOSCOW", "PARIS", "LONDON"]
    for city_name in cities:
        print(coro.send(city_name))
        next(coro)
    coro.close()
