import datetime

from src.job import Job
from src.scheduler import Scheduler
from src.tasks import task_say_hello


def main():
    scheduler = Scheduler()

    my_job = Job(
        target_func=task_say_hello,
        target_func_name=task_say_hello.__name__,
        args=["John"],
        start_at=datetime.datetime.now() + datetime.timedelta(seconds=5),
        max_working_time=10,
        try_count=2,
        dependencies=[],
    )

    scheduler.schedule(job=my_job)
    scheduler.run()
    # scheduler.stop()
    # scheduler.restart()

    # my_job2 = Job(
    #     target_func=task_say_hello,
    #     target_func_name=task_say_hello.__name__,
    #     args=["Bernar"],
    #     max_working_time=10,
    #     try_count=1,
    #     dependencies=[],
    # )
    # scheduler.schedule(job=my_job2)
    # scheduler.run()


if __name__ == "__main__":
    main()
