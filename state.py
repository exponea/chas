import datetime

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
