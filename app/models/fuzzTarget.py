from app.models.fuzzConfig import FuzzConfig

import subprocess
import shlex
import os

# 定義 FuzzTarget 類別


class FuzzTarget:
    def __init__(self, name: str, binaryPath: str, fuzzConfig: FuzzConfig):
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

        env = os.environ.copy()
        env['AFL_AUTORESUME'] = '1'
        env['AFL_I_DONT_CARE_ABOUT_MISSING_CRASHES'] = '1'
        command = f"AFLplusplus/afl-fuzz -i {self.binaryPath}/input -o {self.binaryPath}/output {self.binaryPath}/{binary_file}"
        self.process = subprocess.Popen(shlex.split(
            command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)

        return

    def stop(self) -> None:
        if self.process is not None:
            self.process.kill()
            self.process = None
        return
