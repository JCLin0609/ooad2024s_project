from pathlib import Path
from flask import current_app
from werkzeug.datastructures import FileStorage
from app.Repository.IRepository import IRepository
import json


class UploadService:
    def __init__(self, repository: IRepository):
        self.repository = repository

    def upload_fuzz_Target(self, file: FileStorage, is_input_by_file: bool) -> bool:
        path = Path(current_app.config['UPLOAD_FOLDER']) / file.filename
        config_json = json.dumps({'isInputByFile': is_input_by_file}, indent=4)
        return self.repository.save(file, path, config_json)
