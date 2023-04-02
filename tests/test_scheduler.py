from unittest.mock import patch

from src.utils.enums import JobStatus


def test_scheduler_add_job(simple_scheduler, simple_job):
    simple_scheduler.schedule(job=simple_job)
    assert len(simple_scheduler.jobs) == 1


def test_scheduler_count_by_status(simple_scheduler, simple_job):
    simple_scheduler.schedule(job=simple_job)
    assert simple_scheduler.count_by_status(JobStatus.IN_QUEUE) == 1


def test_scheduler_stop(simple_scheduler, simple_job):
    simple_scheduler.schedule(job=simple_job)
    simple_scheduler.stop()
    assert simple_scheduler.jobs == []


@patch("src.scheduler.Scheduler.run")
def test_scheduler_restart(run_method, simple_scheduler, simple_job):
    simple_scheduler.schedule(job=simple_job)
    simple_scheduler.stop()
    simple_scheduler.restart()
    assert run_method.call_count == 1
    assert len(simple_scheduler.jobs) == 1
