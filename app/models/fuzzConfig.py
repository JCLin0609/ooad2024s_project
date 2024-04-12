from typing import Dict

# 定義 FuzzConfig 類別
class FuzzConfig:
    def __init__(self, configParams: Dict[str, str]):
        self.configParams = configParams