from src.job import Job

# from src.utils.decorators import coroutine


class Scheduler:
    """Scheduler of jobs."""

    def __init__(self, pool_size: int = 10):
        self.pool_size = pool_size
        self.jobs: list[Job] = []

    def schedule(self, job: Job):
        """Add new job to scheduler."""
        print("Add new job to scheduler.")
        self.jobs.append(job)

    def run(self):
        """Run scheduler."""
        print("Run scheduler.")

        while self.jobs:
            job = self.jobs.pop()
            job.result = job.run()
            if job.result:
                print(f"Job (id={job.id}) result: {job.result}")

    # @coroutine
    # def job_execute(self):

    def restart(self):
        pass

    def stop(self):
        pass
