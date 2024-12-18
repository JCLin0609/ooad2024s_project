from app.models.crash import Crash
from app.models.fuzzData import FuzzData
import app.helper.afl_command_helper as afl_command_helper


class FuzzResult:
    def __init__(self, crashes: list[Crash] = [], fuzzData: list[FuzzData] = []):
        self.__crashes: list[Crash] = crashes
        self.__fuzzData: list[FuzzData] = fuzzData

    @property
    def num_crashes(self) -> int:
        return len(self.__crashes)

    @property
    def get_crashed(self) -> list[Crash]:
        return self.__crashes

    @property
    def num_fuzz_data(self) -> int:
        return len(self.__fuzzData)

    def get_specific_crash(self, id: int) -> Crash:
        for crash in self.__crashes:
            if crash.id == int(id):
                return crash
        return None

    def _plot_imgs(self, target_name: str) -> None:
        afl_command_helper.plot_fuzz_imgs(target_name)

    def gen_target_report(self, target_name: str):
        self._plot_imgs(target_name)
