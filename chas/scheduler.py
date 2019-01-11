import datetime
import logging
import time
import copy
from inspect import getargspec
from chas.exceptions import JobNotFoundException
from chas.state import State
from chas.job import Job, JobThread


logger = logging.getLogger("scheduler")

class Scheduler:
    def __init__(self):
        self.jobs = []
    
    @property
    def is_runnable_job(self):
        return self.jobs[0].should_run
    
    @classmethod
    def sift_down(cls, arr, n, i):
        left_child = 2*i+1
        right_child = 2*i+2
        smallest = i
        # Compare current node with left child
        if left_child < n and arr[left_child] < arr[i]:
            smallest = left_child
        if right_child < n and arr[right_child] < arr[smallest]:
            smallest = right_child
        if smallest != i:
            arr[smallest], arr[i] = arr[i], arr[smallest]
            cls.sift_down(arr, n, smallest)
    
    @classmethod
    def sift_up(cls, arr, i):
        if i == 0: return None
        if i % 2 == 1:
            parent = int((i-1) / 2)
        else:
            parent = int((i-2) / 2)
        if arr[parent] > arr[i]:
            arr[parent], arr[i] = arr[i], arr[parent]
            return cls.sift_up(arr, parent)
        return None
    
    # Decorator method for adding jobs
    def job(self, time):
        logger.debug("Registering job.")
        def register_job(job):
            self.register_job(job, time)
        return register_job
    
    # Decorator for setting up the environment of cron job
    def setup(self):
        logger.debug("Setting up environment.")
        def setup_job(job):
            job()
        return setup_job
    
    def register_job(self, function, time):
        job = Job(function, time)
        hour, minute = list(map(lambda x: int(x), time.split(":")))
        datetime_now = datetime.datetime.now()
        # Job cannot be run today, because it is already too late
        if datetime_now.hour > hour or datetime_now.hour == hour and datetime_now.minute > minute: # TODO: Even when minutes equal, we should schedule it for the next day
            job.schedule_number_of_days_from_today(1)
        # Otherwise schedule it for today
        else:
            job.schedule_number_of_days_from_today(0)
        self.jobs.append(job)
        # Heapify, so that the job soonest to be triggered is first
        self.sift_up(self.jobs, len(self.jobs)-1)
        logger.info("Registered job {}. Next run on {}".format(job.name, job.next_run))

    # Run specific job by a name
    def run_job(self, name):
        for job in self.jobs:
            if name == job.name:
                job_state = State()
                logger.info("Running job {} in thread.".format(job.name))
                job_thread = JobThread(job, job_state)
                job_thread.start()
                return True
        raise JobNotFoundException(name)
    
    # Iterates through all jobs and runs those that should be run by now
    # It does so by checking the job on top of the heap
    def run_jobs(self):
        logger.info("Run all jobs at {}".format(datetime.datetime.now()))
        n = len(self.jobs)
        next_job = self.jobs[0]
        while next_job.should_run:
            logger.info("Running job {}".format(next_job.name))
            job_state = State()
            next_job.run(job_state)
            next_job.schedule_number_of_days_from_today(1)
            self.sift_down(self.jobs, n, 0)
            logger.info("Scheduled next run for job {} on {}".format(next_job.name, next_job.next_run))
            next_job = self.jobs[0]
    
    # For convenience it can return list of sorted jobs
    def get_jobs(self, sorted=True):
        jobs = copy.deepcopy(self.jobs)
        if sorted:
            result = []
            n = len(jobs)
            for i in range(n):
                result.append(jobs.pop(0))
                self.sift_down(jobs, n-i-1, 0)
            return result
        return jobs
