import uuid
from typing import Any, Callable

from src.utils.enums import JobStatus


class Job:
    """Job for scheduler."""

    def __init__(
        self,
        target_func: Callable,
        target_func_name: str,
        args=None,
        kwargs=None,
        start_at="",
        job_id: uuid.UUID | None = None,
        max_working_time: int = -1,
        try_count: int = 0,
        dependencies: list["Job"] | None = None,
        status: JobStatus = JobStatus.CREATED,
        result: Any | None = None,
    ):
        """Init job."""
        self.job_id = job_id if job_id else uuid.uuid4()
        self.target_func = target_func
        self.target_func_name = target_func_name
        self.args = args if args else []
        self.kwargs = kwargs if kwargs else {}
        self.start_at = start_at
        self.max_working_time = max_working_time
        self.try_count = try_count
        self.dependencies = dependencies if dependencies else []
        self.status = status
        self.result = result

    def run(self):
        """Run job."""
        try:
            return self.target_func(*self.args, **self.kwargs)
        except Exception as e:
            print(e)
            return None

    @property
    def is_completed(self) -> bool:
        return self.status == JobStatus.COMPLETED
