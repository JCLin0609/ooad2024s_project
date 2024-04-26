from pathlib import Path
from app.models.fuzzTarget import FuzzTarget
from app.models.fuzzConfig import FuzzConfig

from flask import current_app


class FuzzService:
    def __init__(self):
        self.fuzz_target: list[FuzzTarget] = []
        self.current_target: FuzzTarget = None

    def getFuzzTargetsByName(self, name: str):
        for target in self.fuzz_target:
            if target.name == name:
                return target

    def uploadFuzzTarget(self, file, duration) -> bool:
        try:
            upload_folder = Path(current_app.config['UPLOAD_FOLDER'])
            target_folder = upload_folder / file.filename
            if target_folder.exists():
                return False

            target_folder.mkdir(parents=True, exist_ok=True)
            target_path = target_folder / file.filename
            file.save(str(target_path))
            target_path.chmod(0o777)

            config = {
                "name": file.filename,
                "duration": duration,
            }
            afl_config = FuzzConfig(config, str(target_folder))
            new_target = FuzzTarget(
                file.filename, str(target_folder), afl_config)
            self.fuzz_target.append(new_target)
            return True
        except Exception as e:
            print(f"Error uploading file: {e}")
            return False

    def observeFuzzTarget(self) -> list[str]:
        upload_dir = Path(current_app.config['UPLOAD_FOLDER'])
        fuzz_target_dirs = [p.name for p in upload_dir.iterdir() if p.is_dir()]
        return fuzz_target_dirs

    def startRunningTarget(self, target_name: str) -> bool:
        try:
            if self.current_target is not None:
                self.current_target.stop()
                self.current_target = None

            upload_folder = Path(current_app.config['UPLOAD_FOLDER'])
            target_folder = upload_folder / target_name

            if not target_folder.exists():
                return False

            target = self.getFuzzTargetsByName(target_name)
            if target is None:
                config = FuzzConfig.getConfigPersistence(str(target_folder))
                afl_config = FuzzConfig(config, str(target_folder))
                new_target = FuzzTarget(
                    target_name, str(target_folder), afl_config)
                self.fuzz_target.append(new_target)
                target = new_target

            target.run()
            self.current_target = target
            return True
        except Exception as e:
            print(f"Error transferring running target: {e}")
            return False

    def replayFuzzTarget(self) -> None:
        pass
