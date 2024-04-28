from app.Repository.IRepository import IRepository


class ReportService:
    def __init__(self, repository: IRepository):
        self.repository = repository

    def get_target_names(self) -> list[str]:
        return self.repository.get_all_fuzz_target_names()

    def get_report(self, target_name: str):
        return self.repository.get(target_name)

    def get_plot_imgs(self, target_name: str) -> list[str]:
        target = self.repository.get(target_name)
        target.plot_imgs()
        return self.repository.get_plot_imgs(target_name)
