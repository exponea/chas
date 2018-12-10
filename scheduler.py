import datetime
import schedule
import logging
import time
from inspect import getargspec
from state import State
from job import Job


logger = logging.getLogger("scheduler")

class Scheduler:
    def __init__(self):
        self.jobs = []
        self.history = []
    
    @classmethod
    def heap_sort(cls, arr):
        n = len(arr)
        for i in range(n, -1, -1):
            cls.heapify(arr, n, i)
        for i in range(n):
            smallest = arr.pop(0)
            arr.append(smallest)
            cls.heapify(arr, n-i-1, 0)
    
    @classmethod
    def heapify(cls, arr, n, i):
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
            cls.heapify(arr, n, smallest)
    
    def register_job(self, function, time):
        # Process time to run job, format has to be HH:MM
        hour, minute = list(map(lambda x: int(x), time.split(":")))
        datetime_now = datetime.datetime.now()
        # Job cannot be run today, because it is already too late
        if datetime_now.hour > hour:
            next_run_time = datetime.datetime(datetime_now.year, datetime_now.month, datetime_now.day+1, hour, minute)
        # Otherwise schedule it for today
        else:
            next_run_time = datetime.datetime(datetime_now.year, datetime_now.month, datetime_now.day, hour, minute)
        # Create new job and add it to heap
        job = Job(function, next_run_time)
        self.jobs.append(job)
        # Heapify, so that the job soonest to be triggered is first
        self.heapify(self.jobs, len(self.jobs), len(self.jobs))
        logger.info("Registered job {}. Next run on {}".format(job.name, next_run_time))

    def run_jobs(self):
        logger.info("Run all jobs at {}".format(datetime.datetime.now()))
        for job in self.jobs:
            if job.should_run:
                job_state = State()
                job.run(job_state)
                self.history.append(job_state)
    
    def sort_jobs(self):
        return self.heap_sort(self.jobs)
    
    def check_jobs(self):
        self.sort_jobs()
        for job in self.jobs:
            print("Job {} scheduled on {}.".format(job.name, job.next_run))
