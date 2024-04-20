from typing import Dict

# 定義 FuzzConfig 類別
class FuzzConfig:
    def __init__(self, configParams: Dict[str, str], targetFolder: str):
        self.configParams = configParams
        self.targetFolder = targetFolder
        self.configPersistence()

    def configPersistence(self) -> None:
        with open(f"{self.targetFolder}/config.txt", "w") as file:
            for key, value in self.configParams.items():
                file.write(f"{key}: {value}\n")