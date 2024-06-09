class Crash:
    def __init__(self, id: int, signal_number: int, relative_time: int, execs: int, crashingInput: str, crash_path: str):
        self.id = int(id)
        self.signal_number = int(signal_number)
        self.relative_time = int(relative_time)
        self.execs = int(execs)
        self.crashingInput = crashingInput
        self.crash_path = crash_path

    @property
    def get_data(self) -> dict:
        return {
            "id": self.id,
            "signal_number": self.signal_number,
            "relative_time": self.relative_time,
            "execs": self.execs,
            "crashingInput": self.crashingInput
        }
