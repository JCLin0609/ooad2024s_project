from pathlib import Path
from app.models.fuzzConfig import FuzzConfig
from app.models.fuzzResult import FuzzResult
from app.models.fuzzStatus import FuzzStatus
import app.helper.afl_command_helper as afl_command_helper


class FuzzTarget:
    def __init__(self, name: str, dirPath: Path, fuzzResult: FuzzResult, fuzzStatus: FuzzStatus, fuzzConfig: FuzzConfig = None):
        self.name: str = name
        self.dir_path: Path = dirPath
        self.binary_path: Path = dirPath/name
        self.fuzz_result: FuzzResult = fuzzResult
        self.fuzz_status: FuzzStatus = fuzzStatus
        self.fuzz_config: FuzzConfig = fuzzConfig
        self.process = None
        self.__is_running: bool = None

    def run(self) -> bool:
        return afl_command_helper.run_target(self.name)

    def is_running(self) -> bool:
        if self.__is_running is not None:
            return self.__is_running
        self.__is_running = afl_command_helper.is_target_running(self.name)
        return self.__is_running

    def stop(self) -> None:
        afl_command_helper.stop_target()
        return

    def gen_target_report(self) -> FuzzResult:
        if (self.fuzz_result is None):
            return None
        self.fuzz_result.gen_target_report(self.name)
        return self.fuzz_result

    def delete(self) -> bool:
        return afl_command_helper.delete_target(self.name)

    def check_target_bin(self) -> bool:
        pass

    def replay(self) -> None:
        pass

    def get_target_status(self) -> FuzzStatus:
        pass
