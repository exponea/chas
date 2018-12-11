import datetime
import logging
from inspect import getargspec


logger = logging.getLogger("job")

class Job:
    def __init__(self, function, time):
        self.function = function
        self.next_run = time
        self.last_run = "N/A"
    
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

    def run(self, input_state):
        datetime_now = datetime.datetime.now()
        logger.info("Running job {} at {}".format(self.name, datetime_now))
        # Check whether function uses state parameter
        if self.uses_state:
            output_state = self.function(input_state)
        else:
            output_state = self.function()
        self.last_run = datetime_now
        return output_state