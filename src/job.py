import uuid
from typing import Callable


class Job:
    """Job for scheduler."""

    def __init__(
        self,
        target_func: Callable,
        args=None,
        kwargs=None,
        start_at="",
        max_working_time: int = -1,
        try_count: int = 0,
        dependencies=None,
    ):
        """Init job."""
        self.id = uuid.uuid4()
        self.target_func = target_func
        self.args = args if args else []
        self.kwargs = kwargs if kwargs else {}
        self.start_at = start_at
        self.max_working_time = max_working_time
        self.try_count = try_count
        self.dependencies = dependencies if dependencies else []
        self.result = None

    def run(self):
        """Run job."""
        try:
            return self.target_func(*self.args, **self.kwargs)
        except Exception as e:
            print(e)
            return None

    def pause(self):
        pass

    def stop(self):
        pass
