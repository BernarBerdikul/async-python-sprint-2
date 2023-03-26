from enum import Enum


class JobStatus(Enum):
    """Job status."""

    CREATED = 0
    IN_QUEUE = 1
    IN_PROGRESS = 2
    COMPLETED = 3
    ERROR = 4
