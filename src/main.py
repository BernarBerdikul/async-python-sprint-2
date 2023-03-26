from src.job import Job
from src.scheduler import Scheduler
from src.tasks import say_hello


def main():
    scheduler = Scheduler()

    my_job = Job(
        target_func=say_hello,
        target_func_name=say_hello.__name__,
        args=["John"],
        max_working_time=10,
        try_count=1,
        dependencies=[],
    )

    scheduler.schedule(job=my_job)
    scheduler.stop()
    scheduler.restart()

    my_job2 = Job(
        target_func=say_hello,
        target_func_name=say_hello.__name__,
        args=["Bernar"],
        max_working_time=10,
        try_count=1,
        dependencies=[],
    )
    scheduler.schedule(job=my_job2)
    scheduler.run()


if __name__ == "__main__":
    main()
