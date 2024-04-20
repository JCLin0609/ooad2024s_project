from typing import Dict
import os

# 定義 FuzzConfig 類別
class FuzzConfig:
    def __init__(self, configParams: Dict[str, str], targetFolder: str):
        self.configParams = configParams
        self.targetFolder = targetFolder
        self.setConfigPersistence()
        
    def setConfigPersistence(self) -> None:
        if not os.path.exists(f"{self.targetFolder}/config.txt"):
            with open(f"{self.targetFolder}/config.txt", "w") as file:
                for key, value in self.configParams.items():
                    file.write(f"{key}: {value}\n")