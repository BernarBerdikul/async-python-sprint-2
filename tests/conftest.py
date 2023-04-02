import datetime
import shutil
from pathlib import Path
from typing import Generator

import pytest

from src.job import Job
from src.tasks import task_create_dirs, task_say_hello


@pytest.fixture(scope="function")
def created_dirs():
    # Create dirs
    dirs_for_creation: list[str] = ["demo", "beta", "omega", "alpha", "gamma"]
    created_dirs: list[Path] = []
    coro: Generator = task_create_dirs()
    for dir_name in dirs_for_creation:
        created_dirs.append(coro.send(dir_name))
        next(coro)
    coro.close()

    yield created_dirs

    # Delete created dirs
    for created_dir in created_dirs:
        if created_dir.exists():
            shutil.rmtree(created_dir)


@pytest.fixture(scope="function")
def simple_job():
    job = Job(
        target_func=task_say_hello,
        target_func_name=task_say_hello.__name__,
        args=["John"],
        start_at=datetime.datetime.now() + datetime.timedelta(seconds=5),
        max_working_time=10,
        try_count=2,
        dependencies=[],
    )
    return job
