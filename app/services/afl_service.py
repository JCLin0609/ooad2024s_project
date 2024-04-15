from app.models import user
from flask import current_app
import os


class FuzzService:
    def __init__(self):
        self.john = user.User('John', 30)
        self.jane = user.User('Jane', 25)
        self.jclin = user.User('Jclin', 24)

    # Test method
    def users(self):
        return [self.john, self.jane, self.jclin]

    def uploadFuzzTarget(self, file) -> bool:
        try:
            upload_folder = current_app.config['UPLOAD_FOLDER']
            target_folder = os.path.join(upload_folder, file.filename)
            if os.path.exists(target_folder):
                print(f"Folder {target_folder} already exists.")
                return False

            os.makedirs(target_folder)
            file.save(os.path.join(target_folder, file.filename))
            return True
        except Exception as e:
            print(f"Error uploading file: {e}")
            return False

    def transferRunningTarget(self) -> bool:
        pass

    def replayFuzzTarget(self) -> None:
        pass
