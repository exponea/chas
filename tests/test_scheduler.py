import datetime
from src.scheduler import Scheduler
from src.job import Job

# Test scenario when job is executed find the soonest job to run
# Used in updating the heap
def test_sift_down(create_scheduler_with_jobs):
    scheduler = create_scheduler_with_jobs
    assert scheduler.jobs[0].name == "job_e"
    jobs_sorted_order = ["job_e", "job_c", "job_a", "job_b", "job_d"]
    n = len(jobs_sorted_order)
    for i in range(n):
        next_job = scheduler.jobs.pop(0)
        assert jobs_sorted_order[i] == next_job.name
        scheduler.sift_down(scheduler.jobs, n-i-1, 0)


# Create a job which will run the soonest and let it propagate up
# Used in registering new jobs
def test_sift_up(create_scheduler_with_jobs):
    scheduler = create_scheduler_with_jobs
    def job_f():
        return None
    job_f_time = datetime.datetime.now() + datetime.timedelta(minutes=2)
    job_f_hours, job_f_minutes = job_f_time.hour, job_f_time.minute
    job = Job(job_f, str(job_f_hours)+":"+str(job_f_minutes))
    job.next_run = job_f_time
    scheduler.jobs.append(job)
    scheduler.sift_up(scheduler.jobs, len(scheduler.jobs)-1)
    assert scheduler.jobs[0].name == "job_f"

