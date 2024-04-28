from pathlib import Path
from app.models.fuzzConfig import FuzzConfig
from app.models.fuzzResult import FuzzResult
from app.models.fuzzStatus import FuzzStatus
import app.helper.afl_command_helper as afl_command_helper


class FuzzTarget:
    def __init__(self, name: str, dirPath: Path, fuzzResult: FuzzResult, fuzzStatus: FuzzStatus, fuzzConfig: FuzzConfig = None):
        self.name: str = name
        self.dirPath: Path = dirPath
        self.binaryPath: Path = dirPath/name
        self.fuzzResult: FuzzResult = fuzzResult
        self.fuzzStatus: FuzzStatus = fuzzStatus
        self.fuzzConfig: FuzzConfig = fuzzConfig
        self.process = None
        self.__isRunning: bool = None

    def run(self) -> bool:
        return afl_command_helper.run_target(self.name)

    def isRunning(self) -> bool:
        if self.__isRunning is not None:
            return self.__isRunning
        self.__isRunning = afl_command_helper.is_target_running(self.name)
        return self.__isRunning

    def stop(self) -> None:
        afl_command_helper.stop_target()
        return

    def plot_imgs(self) -> None:
        self.fuzzResult.plot_imgs(self.name)
        return
