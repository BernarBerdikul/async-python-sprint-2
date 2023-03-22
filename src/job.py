class Job:
    """Задача для планировщика"""

    def __init__(
        self,
        target_func,
        start_at="",
        max_working_time: int = -1,
        try_count: int = 0,
        dependencies=None,
    ):
        self.target_func = target_func
        self.start_at = start_at
        self.max_working_time = max_working_time
        self.try_count = try_count
        if dependencies is None:
            dependencies = []
        self.dependencies = dependencies
        self.result = None

    def run(self):
        try:
            self.result = self.target_func()
        except Exception as e:
            print(e)

    def pause(self):
        pass

    def stop(self):
        pass
