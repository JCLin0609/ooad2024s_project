from typing import List

import app.models.crash as Crash
import app.models.fuzzData as FuzzData
import app.models.fuzzStatus as FuzzStatus

class FuzzResult:
    def __init__(self, numCrashes: int, timeConsum: int):
        self.numCrashes = numCrashes
        self.timeConsum = timeConsum
        self.crashes: List[Crash] = []
        self.fuzzStatus = None
        self.fuzzData = []

    def add_crash(self, crash: 'Crash'):
        self.crashes.append(crash)

    def set_status(self, status: 'FuzzStatus'):
        self.fuzzStatus = status

    def add_fuzz_data(self, data: 'FuzzData'):
        self.fuzzData.append(data)