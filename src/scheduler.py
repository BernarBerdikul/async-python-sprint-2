import json
import time
from datetime import datetime
from typing import Any, Generator
from uuid import UUID

from src.job import Job
from src.utils.decorators import coroutine
from src.utils.enums import JobStatus


class Scheduler:
    """Scheduler of jobs."""

    STORAGE_FILE = "jobs.json"
    JOB_FUNC_NAME_MAP: dict[str, object] = {}

    def __init__(self, pool_size: int = 10):
        self.pool_size = pool_size
        self.jobs: list[Job] = []

    def schedule(self, job: Job):
        """Add new job to scheduler."""
        print(f"Add job (id={job.job_id}) to scheduler.")
        if inner_jobs := job.dependencies:
            for inner_job in inner_jobs:
                print(
                    f"Add inner job (id={inner_job.job_id}, parent={job.job_id}) to scheduler."
                )
                self.schedule(job=inner_job)

        job.status = JobStatus.IN_QUEUE
        self.JOB_FUNC_NAME_MAP[job.target_func_name] = job.target_func
        self.jobs.append(job)

    def run(self):
        """Run scheduler."""
        print("Run scheduler.")

        coro: Generator[Any, Job, None] = self.coro_generator()

        while self.jobs:
            job = self.jobs.pop()
            if job.status == JobStatus.IN_QUEUE:

                print(f"Next task start at {job.start_at}")
                time_to_next_task = (
                    job.start_at.timestamp() - datetime.now().timestamp()
                )

                if time_to_next_task > 0:
                    time.sleep(time_to_next_task)

                if job.check_dependencies_task_is_complete() is False:
                    job.set_next_start_datetime()

                if self.count_by_status(JobStatus.IN_PROGRESS) < self.pool_size:
                    job.status = JobStatus.IN_PROGRESS
                    coro.send(job)
                else:
                    print("Available only 10 jobs in queue")

    @coroutine
    def coro_generator(self) -> Generator[Any, Job, None]:
        while job := (yield):
            try:
                job.result = job.run()
                job.status = JobStatus.COMPLETED
                print(job.result)
                yield job.result
            except Exception as e:
                print(e)
                if job.try_count > 0:
                    job.try_count -= 1
                    job.status = JobStatus.IN_QUEUE
                else:
                    job.status = JobStatus.ERROR
                    job.result = e

    def count_by_status(self, status: JobStatus) -> int:
        return len([job for job in self.jobs if job.status == status])

    def restart(self):
        """Restart scheduler."""

        print("Load jobs from storage.")
        try:
            with open(self.STORAGE_FILE) as f:
                jobs = json.load(f)
        except Exception as e:
            print(f"Error while loading jobs from storage: {e}.")

        print(f"{len(jobs)} jobs loaded from storage.")
        print("Add jobs to scheduler.")
        for job in jobs:
            job["target_func"] = self.JOB_FUNC_NAME_MAP.get(job["target_func_name"])
            self.schedule(job=Job(**job))

        print("Restart scheduler.")
        self.run()

    def stop(self):
        """Stop scheduler."""

        print("Save jobs in storage.")

        def uuid_convert(o):
            if isinstance(o, UUID):
                return o.hex

        data = []
        for job in self.jobs:
            job_data = job.__dict__
            job_data["dependencies"] = [d.__dict__ for d in job.dependencies]
            data.append(job_data)

        print(f"{len(data)} jobs saved in storage.")
        with open(self.STORAGE_FILE, "w") as f:
            json.dump(data, f, default=uuid_convert)

        print("Scheduler is stopped.")
        self.jobs.clear()
