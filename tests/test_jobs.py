from src.utils.enums import JobStatus


def test_create_job(simple_job):
    assert simple_job is not None
    assert simple_job.target_func is not None
    assert simple_job.args is not None
    assert simple_job.start_at is not None
    assert simple_job.max_working_time is not None
    assert simple_job.try_count is not None
    assert simple_job.dependencies is not None


def test_job_check_dependencies_task_completed(simple_job):
    assert simple_job.status == JobStatus.CREATED
    assert simple_job.check_dependencies_task_completed() is True


def test_job_task_sleep(simple_job):
    current_start_at = simple_job.start_at
    simple_job.make_task_sleep()
    assert current_start_at < simple_job.start_at
