from app.models.crash import Crash
from app.models.fuzzData import FuzzData
import app.helper.afl_command_helper as afl_command_helper


class FuzzResult:
    def __init__(self, crashes: list[Crash] = [], fuzzData: list[FuzzData] = []):
        self.__crashes: list[Crash] = crashes
        self.__fuzzData: list[FuzzData] = fuzzData

    @property
    def numCrashes(self) -> int:
        return len(self.__crashes)

    @property
    def getCrashed(self) -> list[Crash]:
        return self.__crashes

    def _plot_imgs(self, target_name: str) -> None:
        afl_command_helper.plot_fuzz_imgs(target_name)

    def gen_target_report(self, target_name: str):
        self._plot_imgs(target_name)
