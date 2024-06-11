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
        return afl_command_helper.run_target(self)

    def is_running(self) -> bool:
        self.__is_running = afl_command_helper.is_target_running(self.name)
        return self.__is_running

    def is_input_by_file(self) -> bool:
        return self.fuzz_config.is_input_by_file

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
    
    def replay(self, crash_id: int) -> str:
        crash = self.fuzz_result.get_specific_crash(id=crash_id)
        replay_content = afl_command_helper.replay_crash(
            self.name, crash.crash_path, self.is_input_by_file())
        return replay_content