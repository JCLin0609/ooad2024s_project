from app.Repository.IRepository import IRepository


class ReportService:
    def __init__(self, repository: IRepository):
        self.repository = repository

    def get_target_names(self) -> list[str]:
        return self.repository.get_all_fuzz_target_names()
