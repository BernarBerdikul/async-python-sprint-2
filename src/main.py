from src.job import Job
from src.scheduler import Scheduler


def main():
    scheduler = Scheduler()

    my_job = Job(
        target_func=lambda: 1 + 1, max_working_time=10, try_count=1, dependencies=[]
    )

    scheduler.schedule(job=my_job)
    scheduler.run()


if __name__ == "__main__":
    main()
