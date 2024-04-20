from app.models import fuzzResult
from app.models import fuzzConfig

# 定義 FuzzTarget 類別
class FuzzTarget:
    def __init__(self, name: str, binaryPath: str, fuzzConfig: fuzzConfig.FuzzConfig):
        self.name = name
        self.binaryPath = binaryPath
        self.fuzzConfig = fuzzConfig