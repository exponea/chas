import datetime
import logging
import schedule
import time
from scheduler import Scheduler
from inspect import getargspec


class Sisyphus:
    def __init__(self):
        self.scheduler = Scheduler()
    
    def job(self, time):
        def register_job(job):
            self.scheduler.register_job(job, time)
        return register_job
    
    def run_jobs(self):
        return self.scheduler.run_jobs()
    
    def check_jobs(self):
        return self.scheduler.check_jobs()
