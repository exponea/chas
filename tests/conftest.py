import datetime
import pytest
from src.scheduler import Scheduler

# Test jobs
def job_a():
    return None
def job_b():
    return None
def job_c():
    return None
def job_d():
    return None
def job_e():
    return None

@pytest.fixture
def create_scheduler_with_jobs():
    scheduler = Scheduler()
    datetime_now = datetime.datetime.now()
    job_a_time = datetime_now + datetime.timedelta(minutes=10)
    job_b_time = datetime_now + datetime.timedelta(minutes=15)
    job_c_time = datetime_now + datetime.timedelta(minutes=7)
    job_d_time = datetime_now + datetime.timedelta(minutes=19)
    job_e_time = datetime_now + datetime.timedelta(minutes=4)
    job_a_hours, job_a_minutes = job_a_time.hour, job_a_time.minute
    job_b_hours, job_b_minutes = job_b_time.hour, job_b_time.minute
    job_c_hours, job_c_minutes = job_c_time.hour, job_c_time.minute
    job_d_hours, job_d_minutes = job_d_time.hour, job_d_time.minute
    job_e_hours, job_e_minutes = job_e_time.hour, job_e_time.minute
    scheduler.register_job(job_a, str(job_a_hours)+":"+str(job_a_minutes))
    scheduler.register_job(job_b, str(job_b_hours)+":"+str(job_b_minutes))
    scheduler.register_job(job_c, str(job_c_hours)+":"+str(job_c_minutes))
    scheduler.register_job(job_d, str(job_d_hours)+":"+str(job_d_minutes))
    scheduler.register_job(job_e, str(job_e_hours)+":"+str(job_e_minutes))
    return scheduler
