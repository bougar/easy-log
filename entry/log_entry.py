class LogEntry:
    def __init__(self, metadata: dict = {}, data: dict = {}):
        self.metadata = metadata 
        self.data = data