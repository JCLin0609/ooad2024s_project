from app.Repository.IRepository import IRepository


class ReportService:
    def __init__(self, repository: IRepository):
        self.repository = repository

    def get_target_names(self) -> list[str]:
        return self.repository.get_all_fuzz_target_names()

    def get_target_report(self, target_name: str):
        try:
            target = self.repository.get(target_name)
            target_report = target.gen_target_report()
            if target_report is None:
                return None, None
            return target_report
        except Exception as e:
            print(f"Error getting target report: {e}")
            return None

    def get_target_report_img_path(self, target_name: str) -> list[str]:
        return self.repository.get_plot_imgs(target_name)
