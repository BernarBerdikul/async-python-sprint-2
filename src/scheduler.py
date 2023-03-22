from src.job import Job


class Scheduler:
    """Scheduler of jobs."""

    def __init__(self, pool_size: int = 10):
        self.pool_size = pool_size
        self.tasks: list[Job] = []

    def schedule(self, job: Job):
        """Add new job to scheduler."""
        print("Add new job to scheduler")
        self.tasks.append(job)

    def run(self):
        """Run scheduler."""
        print("Run scheduler")

        while self.tasks:
            job = self.tasks.pop()
            job.run()
            if job.result:
                print("Job result:", job.result)

    def restart(self):
        pass

    def stop(self):
        pass
