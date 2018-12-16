import datetime
import logging
from inspect import getargspec
from src.state import State

logger = logging.getLogger("job")

class Job:
    def __init__(self, function, time):
        self.function = function
        self.registered_time = time
        self.next_run = None
        self.last_run = "N/A"
        self.last_state = State()
    
    @property
    def should_run(self):
        return datetime.datetime.now() >= self.next_run

    @property
    def uses_state(self):
        function_spec = getargspec(self.function)
        return "state" in function_spec.args
    
    @property
    def name(self):
        return self.function.__name__
    
    # Override native greater than by comparing times of next run
    def __gt__(self, other):
        if isinstance(other, Job):
            return self.next_run > other.next_run
        return False
    
    # Override native less than by comparing times of next run
    def __lt__(self, other):
        if isinstance(other, Job):
            return self.next_run < other.next_run
        return False
    
    def __str__(self):
        return self.function.__name__

    def run(self, input_state=State()):
        datetime_now = datetime.datetime.now()
        logger.info("Running job {} at {}".format(self.name, datetime_now))
        self.last_run = datetime_now
        self.last_state = input_state
        self.last_state.running()
        # Check whether function uses state parameter
        if self.uses_state:
            self.function(self.last_state)
        else:
            self.function()
        self.last_state.finished()
        return self.last_state
    
    def schedule_number_of_days_from_today(self, days):
        # Process time to run job, format has to be HH:MM
        hour, minute = list(map(lambda x: int(x), self.registered_time.split(":")))
        datetime_now = datetime.datetime.now()
        self.next_run = datetime.datetime(datetime_now.year, datetime_now.month, datetime_now.day+days, hour, minute)
        return self.next_run
    
    def update_next_run_time(self, run_time):
        self.next_run = run_time
