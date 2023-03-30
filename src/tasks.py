import os
import shutil
from pathlib import Path
from typing import Generator

from src.clients.weather_api import get_city_weather
from src.utils.decorators import coroutine

BASE_DIR = Path(__file__).resolve().parent.parent


@coroutine
def task_say_hello() -> Generator[str, str, None]:
    """Task to say hello for specific person."""
    while True:
        try:
            # Get sent data from coroutine
            name: str = yield  # type: ignore
            yield f"Hello {name}!"
        except GeneratorExit:
            print("Close coro for 'task_say_hello'")
            raise


@coroutine
def task_with_network() -> Generator[dict, str, None]:
    """Task to get weather info for specific city."""
    while True:
        try:
            # Get sent data from coroutine
            city_name = yield  # type: ignore
            yield get_city_weather(city_name)
        except GeneratorExit:
            print("Close coro for 'task_with_network'")
            raise


def create_text_file(dir_path: Path, name: str) -> None:
    """Method to create .txt file inside specific dir."""
    with open(dir_path / f"{name}.txt", "w") as f:
        f.write(name)


@coroutine
def task_create_dirs() -> Generator[Path, str, None]:
    """Task for new dir(s) creation."""
    while True:
        try:
            # Get sent data from coroutine
            dir_name = yield  # type: ignore
            # Create new dir by name
            new_dir = BASE_DIR / dir_name
            if not new_dir.exists():
                os.mkdir(new_dir)
            # Create text file inside new dir
            create_text_file(dir_path=new_dir, name=dir_name)
            yield new_dir
        except GeneratorExit:
            print("Close coro for 'task_create_dirs'")
            raise


@coroutine
def task_delete_dirs() -> Generator[bool, str, None]:
    """Task for existed dir(s) removing."""
    while True:
        try:
            # Get sent data from coroutine
            dir_name = yield  # type: ignore
            dir_for_delete = BASE_DIR / dir_name
            is_deleted = dir_for_delete.exists()

            yield is_deleted

            if is_deleted:
                shutil.rmtree(dir_for_delete)
        except GeneratorExit:
            print("Close coro for 'task_delete_dirs'")
            raise
