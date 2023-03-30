from pathlib import Path
from typing import Generator
from unittest.mock import patch

from src.tasks import (
    task_create_dirs,
    task_delete_dirs,
    task_say_hello,
    task_with_network,
)


def test_task_with_network():
    cities = ["MOSCOW", "PARIS", "LONDON"]
    data = []
    coro: Generator = task_with_network()
    for city_name in cities:
        data.append(coro.send(city_name))
        next(coro)
    coro.close()
    assert len(data) == len(cities)


def test_task_sey_hello():
    name = "Bernar"
    expected_data = f"Hello {name}!"
    coro: Generator = task_say_hello()
    result = coro.send(name)
    next(coro)
    coro.close()
    assert result == expected_data


@patch("src.tasks.create_text_file")
def test_task_create_dirs(create_text_file):
    dirs_for_creation: list[str] = ["demo", "beta", "omega", "alpha", "gamma"]
    result: list[Path] = []
    coro: Generator = task_create_dirs()
    for dir_name in dirs_for_creation:
        result.append(coro.send(dir_name))
        next(coro)
    coro.close()
    # Check dirs are created
    for created_dir in result:
        assert created_dir.exists() is True
    # Check mock 'create_text_file' call params
    for (args, kwargs), dir_path, name in zip(
        create_text_file.call_args_list, result, dirs_for_creation
    ):
        assert kwargs.get("dir_path") == dir_path
        assert kwargs.get("name") == name
    # Check mock 'create_text_file' call count
    assert create_text_file.call_count == len(dirs_for_creation)


@patch("shutil.rmtree")
def test_task_delete_existed_dirs(shutil_rmtree_func, created_dirs):
    dirs_for_removing: list[str] = ["demo", "beta", "omega", "alpha", "gamma"]

    result: list[bool] = []
    coro: Generator = task_delete_dirs()
    for dir_name in dirs_for_removing:
        result.append(coro.send(dir_name))
        next(coro)
    coro.close()
    # Check result
    assert all(result) is True
    # Check mock 'shutil_rmtree_func' call count
    assert shutil_rmtree_func.call_count == len(dirs_for_removing)


@patch("shutil.rmtree")
def test_task_delete_not_existed_dirs(shutil_rmtree_func):
    dirs_for_removing: list[str] = ["demo", "beta", "omega", "alpha", "gamma"]
    result: list[bool] = []
    coro: Generator = task_delete_dirs()
    for dir_name in dirs_for_removing:
        result.append(coro.send(dir_name))
        next(coro)
    coro.close()
    # Check result
    assert all(result) is False
    # Check mock 'shutil_rmtree_func' call count
    assert shutil_rmtree_func.call_count == 0
