import datetime
import logging
import uuid
from typing import Callable, Generator, Self

from src.utils.enums import JobStatus

logger = logging.getLogger(__name__)


class Job:
    """Job for scheduler."""

    def __init__(
        self,
        target_func: Callable,
        args=None,
        kwargs=None,
        start_at=datetime.datetime.now(),
        job_id: uuid.UUID | None = None,
        max_working_time: int = -1,
        try_count: int = 0,
        dependencies: list[Self] | None = None,
        status: JobStatus = JobStatus.CREATED,
        result=None,
    ):
        """Init job."""
        self.job_id = job_id or uuid.uuid4()
        self.target_func = target_func
        self.args = args if args else []
        self.kwargs = kwargs if kwargs else {}
        self.start_at = start_at
        self.max_working_time = max_working_time
        self.try_count = try_count
        self.dependencies = dependencies if dependencies else []
        self.status = status
        self.result = result if result else []

    def run(self) -> None:
        """Run job."""
        try:
            logger.info(
                f"Job [id={self.job_id}] get params: args={self.args}, kwargs={self.kwargs}."
            )
            coro: Generator = self.target_func()
            for arg in self.args:
                answer = coro.send(arg)
                self.result.append(answer)
            for kwarg in self.kwargs:
                answer = coro.send(kwarg)
                self.result.append(answer)
            coro.close()
            logger.info(f"Job id={self.job_id} result: {self.result}")
        except Exception as e:
            logger.error(e)

    def check_dependencies_task_completed(self) -> bool:
        return all(
            [
                dependencies_task.status == JobStatus.COMPLETED
                for dependencies_task in self.dependencies
            ]
        )

    def make_task_sleep(self) -> None:
        self.start_at += datetime.timedelta(minutes=5)
