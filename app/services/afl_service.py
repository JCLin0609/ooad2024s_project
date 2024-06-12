from app.Repository.IRepository import IRepository
from app.models.fuzzTarget import FuzzTarget


class AFLService:
    def __init__(self, repository: IRepository):
        self.repository = repository

    def current_running_target(self) -> FuzzTarget:
        targets = self.repository.get_all()
        for target in targets:
            if target.is_running():
                return target
        return None

    def current_running_target_name(self) -> str:
        target = self.current_running_target()
        if target is None:
            return None
        return target.name

    def start_running_target(self, target_name: str) -> bool:
        try:
            target = self.repository.get(target_name)
            if target is None:
                return False
            return target.run()
        except Exception as e:
            print(f"Error transferring running target: {e}")
            return False

    def stop_running_target(self) -> bool:
        target = self.current_running_target()
        if target is None:
            return False
        target.stop()
        return True

    def delete_target(self, target_name: list[str]) -> bool:
        try:
            for name in target_name:
                target = self.repository.get(name)
                if target is None:
                    return False
                target.delete()
            return True
        except Exception as e:
            print(f"Error deleting target: {e}")
            return False
