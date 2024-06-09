from werkzeug.datastructures import FileStorage
from pathlib import Path
from abc import ABC, abstractmethod
from app.models.fuzzTarget import FuzzTarget


class IRepository(ABC):
    @abstractmethod
    def save(self, file: FileStorage, path: Path, config_json: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get(self, target_name: str) -> FuzzTarget:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[FuzzTarget]:
        raise NotImplementedError

    @abstractmethod
    def get_all_fuzz_target_names(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def get_plot_imgs(self, target_name: str) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, target_name: str) -> bool:
        raise NotImplementedError
