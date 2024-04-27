from app.models.crash import Crash
from app.models.fuzzData import FuzzData


class FuzzResult:
    def __init__(self, crashes: list[Crash] = [], fuzzData: list[FuzzData] = []):
        self.__crashes: list[Crash] = crashes
        self.__fuzzData: list[FuzzData] = fuzzData

    @property
    def numCrashes(self) -> int:
        return len(self.__crashes)
