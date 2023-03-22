from src.job import Job
from src.scheduler import Scheduler


def say_hello(name: str):
    return f"Hello {name}!"


def main():
    scheduler = Scheduler()

    my_job = Job(
        target_func=say_hello,
        args=["John"],
        max_working_time=10,
        try_count=1,
        dependencies=[],
    )

    scheduler.schedule(job=my_job)
    scheduler.run()


if __name__ == "__main__":
    main()
