import json
from uuid import UUID

from src.job import Job
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
        job.status = JobStatus.IN_QUEUE
        self.JOB_FUNC_NAME_MAP[job.target_func_name] = job.target_func
        self.jobs.append(job)

    def run(self):
        """Run scheduler."""
        print("Run scheduler.")

        while self.jobs:
            job = self.jobs.pop()
            job.result = job.run()
            if job.result:
                print(f"Job (id={job.job_id}) result: {job.result}")

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
