import datetime
import logging
import schedule
import time
from inspect import getargspec

logging.basicConfig()
logger = logging.getLogger("sisyphus")
logger.setLevel("WARNING")
logger.info("Initialized sisyphus.")

class Job:
    def __init__(self, function, time):
        self.time = time
        self.function = function
        self.next_run = None
        self.last_run = None
        self._update_next_run_time()
    
    @property
    def should_run(self):
        # return datetime.datetime.now() >= self.next_run
        return True

    @property
    def uses_state(self):
        function_spec = getargspec(self.function)
        return "state" in function_spec.args
    
    # Override native greater than by comparing times of next run
    def __gt__(self, other):
        if isinstance(other, Job):
            return self.next_run > other.next_run
        return False
    
    # Override native less than by comparing times of next run
    def __lt__(self, other):
        if isinstance(other, Job):
            return self.next_run > other.next_run
        return False
    
    def __str__(self):
        return self.function.__name__
    
    def _update_next_run_time(self):
        hour, minute = list(map(lambda x: int(x), self.time.split(":")))
        datetime_now = datetime.datetime.now()
        datetime_today_job = datetime.datetime(datetime_now.year, datetime_now.month, datetime_now.day, hour, minute)
        if datetime_now.hour > hour:
            self.next_run = datetime_today_job + datetime.timedelta(1)
        elif self.last_run is not None and datetime_now - self.last_run < datetime.timedelta(0.5):
            self.next_run = datetime_today_job + datetime.timedelta(1)
        else:
            self.next_run = datetime_today_job
        logger.info("Schedule run for {}".format(self.next_run))

    def run(self, input_state):
        datetime_now = datetime.datetime.now()
        logger.info("Running job {} at {}".format(self, datetime_now))
        # Check whether function uses state parameter
        if self.uses_state:
            output_state = self.function(input_state)
        else:
            output_state = self.function()
        self.last_run = datetime_now
        self._update_next_run_time()
        return output_state

class State:
    def __init__(self):
        self.status = "Not triggered"
        self.detail = None
        self.timestamp_created = int(datetime.datetime.now().timestamp())
        self.timestamp_finished = None
            
    def success(self):
        self.set_status("Success")
        return self
    
    def fail(self):
        self.set_status("Fail")
        return self
    
    def result(self, res):
        self.detail = res
        return self
    
    def get_result(self):
        return self.detail
    
    def set_status(self, status):
        self.status = status
    
    def get_status(self):
        return self.status

class Scheduler:
    def __init__(self):
        self.jobs = []
        self.history = []
    
    @classmethod
    def heap_sort(cls, arr):
        n = len(arr)
        for i in range(n, -1, -1):
            cls.heapify(n, i)
    
    @classmethod
    def heapify(cls, arr, i):
        n = len(arr)
        left_child = 2*i+1
        right_child = 2*i+2
        smallest = i
        # Compare current node with left child
        if left_child < n and arr[left_child] < arr[i]:
            smallest = left_child
        if right_child < n and arr[right_child] < arr[smallest]:
            smallest = right_child
        if not smallest == i:
            arr[smallest], arr[i] = arr[i], arr[smallest]
            cls.heapify(n, smallest)
    
    def register_job(self, job, time):
        self.jobs.append(Job(job, time))

    def run_jobs(self):
        logger.info("Check all jobs at {}".format(datetime.datetime.now()))
        for job in self.jobs:
            if job.should_run:
                job_state = State()
                # job.run(job_state)
                job.run(test_state)
                self.history.append(job_state)
    

class Sisyphus:
    def __init__(self):
        self.scheduler = Scheduler()
    
    def job(self, time):
        def register_job(job):
            self.scheduler.register_job(job, time)
        return register_job
    
    def run_jobs(self):
        self.scheduler.run_jobs()

sisyphus = Sisyphus()
test_state = State()

@sisyphus.job("17:59")
def export_a(state):
    print("Previous state: " + state.get_status())
    print(state.get_result())
    if state.status == "Success":
        state.fail().result("100")
    else:
        state.success().result("200")

while True:
    time.sleep(1)
    sisyphus.run_jobs()


