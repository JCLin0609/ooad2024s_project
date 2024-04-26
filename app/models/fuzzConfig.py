from pathlib import Path

# Define FuzzConfig class


class FuzzConfig:
    def __init__(self, config_params: dict[str, str], target_folder: str):
        self.config_params = config_params
        self.target_folder = target_folder
        self.setConfigPersistence()

    def setConfigPersistence(self) -> None:
        config_file = Path(self.target_folder) / "config.txt"
        if not config_file.exists():
            with config_file.open("w") as file:
                for key, value in self.config_params.items():
                    file.write(f"{key}: {value}\n")

    @classmethod
    def getConfigPersistence(cls, target_folder: str) -> dict[str, str]:
        config_params = {}
        config_file = Path(target_folder) / "config.txt"
        if config_file.exists():
            with config_file.open("r") as file:
                for line in file:
                    key, value = line.strip().split(": ")
                    config_params[key] = value
        return config_params
