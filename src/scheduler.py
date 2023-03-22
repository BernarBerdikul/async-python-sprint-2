from src.job import Job


class Scheduler:
    """Планировщик задач"""

    def __init__(self, pool_size: int = 10):
        self.pool_size = pool_size
        self.tasks: list[Job] = []

    def schedule(self, task):
        pass

    def run(self):
        pass

    def restart(self):
        pass

    def stop(self):
        pass
