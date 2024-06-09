from app.Repository.IRepository import IRepository


class ReplayService:
    def __init__(self, repository: IRepository):
        self.repository = repository

    def replay_target(self, target_name: str, crash_id: int) -> str:
        target = self.repository.get(target_name)
        replay_content = target.replay(crash_id)
        return replay_content
