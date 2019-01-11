class JobNotFoundException(Exception):
    def __init__(self, job_name):
        super().__init__("Job {} was not found.".format(job_name))
        self.errors = job_name