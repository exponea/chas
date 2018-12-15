import datetime

class State:
    def __init__(self):
        self.status = "N/A"
        self.detail = None
        self.timestamp_created = int(datetime.datetime.now().timestamp())
        self.timestamp_finished = None
            
    def success(self):
        self.set_status("Succeeded")
        return self
    
    def failed(self):
        self.set_status("Failed")
        return self
    
    def running(self):
        self.set_status("Running")
        return self
    
    def finished(self):
        if self.status not in ["Succeeded", "Failed"]:
            self.set_status("Finished")
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
