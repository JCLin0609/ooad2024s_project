from app.Repository.IRepository import IRepository
from app.models.fuzzTarget import FuzzTarget


class AFLService:
    def __init__(self, repository: IRepository):
        self.repository = repository

    def current_running_target(self) -> FuzzTarget:
        targets = self.repository.get_all()
        for target in targets:
            if target.isRunning():
                return target

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
        return target.stop()

    def replay_fuzz_target(self) -> None:
        pass
