from app.models import fuzzResult
from app.models import fuzzConfig

import subprocess
import shlex
import os

# 定義 FuzzTarget 類別
class FuzzTarget:
    def __init__(self, name: str, binaryPath: str, fuzzConfig: fuzzConfig.FuzzConfig):
        self.name = name
        self.binaryPath = binaryPath
        self.fuzzConfig = fuzzConfig
        self.process = None

    def run(self) -> None:
        if not os.path.exists(os.path.join(self.binaryPath, 'input')):
            os.makedirs(os.path.join(self.binaryPath, 'input'))
            with open(os.path.join(self.binaryPath, 'input', 'seed.txt'), 'w') as f:
                f.write("-")

        binary_file = os.path.basename(self.binaryPath)
        
        command = f"AFLplusplus/afl-fuzz -i {self.binaryPath}/input -o {self.binaryPath}/output {self.binaryPath}/{binary_file}"
        command = shlex.split(command)
        self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return

    def stop(self) -> None:
        if self.process is not None:
            self.process.kill()
            self.process = None
        return
