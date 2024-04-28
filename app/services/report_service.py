from app.Repository.IRepository import IRepository


class ReportService:
    def __init__(self, repository: IRepository):
        self.repository = repository

    def get_target_names(self) -> list[str]:
        return self.repository.get_all_fuzz_target_names()

    def get_report(self, target_name: str):
        return self.repository.get(target_name)

    def get_target_report(self, target_name: str):
        try:
            target = self.repository.get(target_name)
            target_report = target.gen_target_report()
            target_report_img_path = self.repository.get_plot_imgs(target_name)
            return target_report, target_report_img_path
        except Exception as e:
            print(f"Error getting target report: {e}")
            return None, None
