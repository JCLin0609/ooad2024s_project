from datetime import datetime

class FuzzStatus:
    def __init__(self, startTime: datetime, lastUpdate: datetime, fuzzerPid: int, corpusCount: int, lastFind: datetime, lastCrash: datetime):
        self.startTime = startTime
        self.lastUpdate = lastUpdate
        self.fuzzerPid = fuzzerPid
        self.corpusCount = corpusCount
        self.lastFind = lastFind
        self.lastCrash = lastCrash

    def update(self, lastUpdate: datetime, corpusCount: int, lastFind: datetime, lastCrash: datetime):
        self.lastUpdate = lastUpdate
        self.corpusCount = corpusCount
        self.lastFind = lastFind
        self.lastCrash = lastCrash