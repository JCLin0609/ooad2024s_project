class Crash:
    def __init__(self, signal_number: int, relative_time: int, execs: int, crashingInput: str):
        self.signal_number = signal_number
        self.relative_time = relative_time
        self.execs = execs
        self.crashingInput = crashingInput
