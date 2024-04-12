import app.models.fuzzResult as FuzzResult

# 定義 FuzzTarget 類別
class FuzzTarget:
    def __init__(self, name: str, binaryPath: str):
        self.name = name
        self.binaryPath = binaryPath