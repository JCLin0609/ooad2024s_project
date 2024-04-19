from app.models import user
from app.models import fuzzTarget
from flask import current_app
import os

class FuzzService:
    def __init__(self):
        self.john = user.User('John', 30)
        self.jane = user.User('Jane', 25)
        self.jclin = user.User('Jclin', 24)
        self.fuzz_target = []

    # Test method
    def users(self):
        return [self.john, self.jane, self.jclin]
    
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
            file.save(os.path.join(target_folder, file.filename))
            
            self.fuzz_target.append(fuzzTarget.FuzzTarget(file.filename, target_folder))
            return True
        except Exception as e:
            print(f"Error uploading file: {e}")
            return False

    def transferRunningTarget(self) -> bool:
        pass

    def replayFuzzTarget(self) -> None:
        pass
