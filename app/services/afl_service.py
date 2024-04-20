from app.models import fuzzTarget
from app.models import fuzzConfig

from flask import current_app
import os

class FuzzService:
    def __init__(self):
        self.fuzz_target = []
        self.current_target = None
    
    def getfuzzTargetsByName(self, name):
        for target in self.fuzz_target:
            if target.name == name:
                return target

    def uploadFuzzTarget(self, file, duration) -> bool:
        try:
            upload_folder = current_app.config['UPLOAD_FOLDER']
            target_folder = os.path.join(upload_folder, file.filename)
            if os.path.exists(target_folder):
                print(f"Folder {target_folder} already exists.")
                return False

            os.makedirs(target_folder)
            target_path = os.path.join(target_folder, file.filename)
            file.save(target_path)
            os.chmod(target_path, 0o777)
            
            config = {
                "name": file.filename,
                "duration": duration,
            }
            AflConfig = fuzzConfig.FuzzConfig(config, target_folder)

            new_target = fuzzTarget.FuzzTarget(file.filename, target_folder, AflConfig)
            self.fuzz_target.append(new_target)

            return True
        except Exception as e:
            print(f"Error uploading file: {e}")
            return False

    def observeFuzzTarget(self) -> list:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        targetNameList = [name for name in os.listdir(upload_folder) if os.path.isdir(os.path.join(upload_folder, name))]
        return targetNameList

    def startRunningTarget(self, targetName) -> bool:
        try:
            if(self.current_target is not None):
                self.current_target.stop()
                self.current_target = None
            upload_folder = current_app.config['UPLOAD_FOLDER']
            target_folder = os.path.join(upload_folder, targetName)
            if not os.path.exists(target_folder):
                print(f"Folder {target_folder} does not exist.")
                return False
            
            target = self.getfuzzTargetsByName(targetName)
            if target is None:
                config = fuzzConfig.FuzzConfig.getConfigPersistence(target_folder)
                AflConfig = fuzzConfig.FuzzConfig(config, target_folder)
                new_target = fuzzTarget.FuzzTarget(targetName, target_folder, AflConfig)
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
