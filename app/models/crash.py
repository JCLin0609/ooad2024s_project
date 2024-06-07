class Crash:
    def __init__(self, num: int, id: int, signal_number: int, relative_time: int, execs: int, crashingInput: str, crash_path: str):
        self.num = num
        self.id = id
        self.signal_number = signal_number
        self.relative_time = relative_time
        self.execs = execs
        self.crashingInput = crashingInput
        self.crash_path = crash_path

    @property
    def get_data(self) -> dict:
        return {
            "num": self.num,
            "id": self.id,
            "signal_number": self.signal_number,
            "relative_time": self.relative_time,
            "execs": self.execs,
            "crashingInput": self.crashingInput
        }
