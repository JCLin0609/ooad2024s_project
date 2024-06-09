import shutil
from werkzeug.datastructures import FileStorage
from app.Repository.IRepository import IRepository
from app.models.crash import Crash
from app.models.fuzzData import FuzzData
from app.models.fuzzResult import FuzzResult
from app.models.fuzzStatus import FuzzStatus
from app.models.fuzzTarget import FuzzTarget
from app.models.fuzzConfig import FuzzConfig
from pathlib import Path
from flask import current_app


class FuzzTargetRepository(IRepository):
    def save(self, file: FileStorage, path: Path, config_json: str) -> bool:
        if file is None or file.filename is None or file.filename == '' or path.exists():
            return False
        try:
            path.mkdir(parents=True, exist_ok=True)
            save_path = path / file.filename
            file.save(save_path)
            save_path.chmod(0o777)
            self.__set_default_dir_and_seed(path)
            self.__set_config_json(path, config_json)
            return True
        except Exception as e:
            return False

    def get(self, target_name: str) -> FuzzTarget | None:
        target_dir = Path(current_app.config['UPLOAD_FOLDER'])
        target_path = target_dir / target_name
        if not target_path.exists():
            return None

        fuzz_result = self.__get_fuzz_result_by_name(target_name)
        fuzz_status = self.__get_fuzz_status_by_name(target_name)
        fuzz_config = self.__get_fuzz_config_by_name(target_name)
        return FuzzTarget(
            target_name, target_path, fuzz_result, fuzz_status, fuzz_config)

    def get_all(self) -> list[FuzzTarget]:
        names = self.get_all_fuzz_target_names()
        targets = []
        for name in names:
            target = self.get(name)
            if target:
                targets.append(target)
        return targets

    def get_all_fuzz_target_names(self) -> list[str]:
        target_dir = Path(current_app.config['UPLOAD_FOLDER'])
        return [str(dir.name) for dir in target_dir.iterdir() if dir.is_dir()]

    def get_plot_imgs(self, target_name: str) -> list[str]:
        target_img_dir = Path(
            current_app.config['TARGET_IMG_FOLDER']) / target_name
        if not target_img_dir.exists():
            return []
        return [img.name for img in target_img_dir.iterdir() if img.name.endswith(('.png', '.jpg'))]

    def delete(self, target_name: str) -> bool:
        target = Path(current_app.config['UPLOAD_FOLDER']) / target_name
        if target.exists():
            try:
                shutil.rmtree(target)
                return True
            except Exception as e:
                return False
        return False

    def __set_default_dir_and_seed(self, dirPath: Path):
        input_dir = dirPath / 'input'
        if not input_dir.exists():
            input_dir.mkdir(parents=True)
            with open(input_dir / 'seed.txt', 'w') as f:
                f.write("-")

    def __set_config_json(self, path: Path, config_json: str):
        with open(path / 'config.json', 'w') as f:
            f.write(config_json)

    def __get_fuzz_status_by_name(self, name: str) -> FuzzStatus:
        fuzzer_stats = Path(
            current_app.config['UPLOAD_FOLDER']) / name / 'output' / 'default' / 'fuzzer_stats'
        if not fuzzer_stats.exists():
            return None
        return FuzzStatus.from_string(fuzzer_stats.read_text())

    def __get_fuzz_result_by_name(self, name: str) -> FuzzResult:
        target_output_dir = Path(
            current_app.config['UPLOAD_FOLDER']) / name / 'output' / 'default'

        if not target_output_dir.exists():
            return None

        fuzzData = self.__process_fuzz_data(target_output_dir)
        crashes = self.__process_crash_dir(target_output_dir)

        return FuzzResult(fuzzData=fuzzData, crashes=crashes)

    def __get_fuzz_config_by_name(self, name: str) -> FuzzConfig:
        config_json = Path(
            current_app.config['UPLOAD_FOLDER']) / name / 'config.json'
        if not config_json.exists():
            return None
        return FuzzConfig.from_json(config_json.read_text())

    def __process_fuzz_data(self, output_dir: Path) -> list[FuzzData]:
        plot_data = output_dir / 'plot_data'
        fuzz_data_list = []

        if not plot_data.exists():
            return fuzz_data_list
        with plot_data.open('r') as f:
            # Skip the header line
            next(f)

            for line in f:
                data = line.strip().split(',')
                fuzz_data = FuzzData(
                    relativeTime=int(data[0]),
                    cycleDone=int(data[1]),
                    corpusCount=int(data[3]),
                    mapSize=float(data[6].rstrip('%')),
                    savedCrashes=int(data[7]),
                    maxDepth=int(data[9]),
                    execsPerSec=float(data[10]),
                    totalExecs=int(data[11]),
                    edgesFound=int(data[12])
                )
                fuzz_data_list.append(fuzz_data)

        return fuzz_data_list

    def __process_crash_dir(self, target_output_dir: Path) -> list[Crash]:
        crash_dirs = [dir for dir in target_output_dir.iterdir(
        ) if dir.is_dir() and dir.name.startswith('crashes')]
        crash_files = [file for crash_dir in crash_dirs for file in crash_dir.iterdir(
        ) if file.name.startswith('id:')]

        crashes = list[Crash]()
        for crash_file in crash_files:
            crash = self.__process_crash_file(crash_file)
            if crash:
                crashes.append(crash)
                
        crashes.sort(key=lambda x: x.id, reverse=True)
        return crashes

    def __process_crash_file(self, crash_file: Path) -> Crash:
        try:
            file_info = {k: v for k, v in (item.split(
                ':')for item in crash_file.name.split(','))}
            with open(crash_file,  'r', encoding="utf-8", errors='ignore') as f:
                file_content = f.read()
            crash = Crash(
                id=file_info['id'],
                signal_number=file_info['sig'],
                relative_time=file_info['time'],
                execs=file_info['execs'],
                crashingInput=file_content,
                crash_path=crash_file
            )
            return crash
        except (KeyError, ValueError, OSError) as e:
            print(f"Error processing crash file: {crash_file}. Error: {e}")
            return None
