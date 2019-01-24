import datetime

class State:
    def __init__(self):
        self.status = "N/A"
        self.detail = None
        self.timestamp_created = int(datetime.datetime.now().timestamp())
        self.timestamp_finished = None
            
    def success(self, detail=None):
        self.status = "Succeeded"
        if detail is not None:
            self.detail = detail
        return self
    
    def failed(self, detail=None):
        self.status = "Failed"
        if detail is not None:
            self.detail = detail
        return self
    
    def running(self):
        self.status = "Running"
        return self
    
    def finished(self):
        if self.status not in ["Succeeded", "Failed"]:
            self.status = "Finished"
        return self

