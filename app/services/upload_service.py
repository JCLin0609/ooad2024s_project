from pathlib import Path

from flask import current_app
from werkzeug.datastructures import FileStorage

from app.Repository.IRepository import IRepository


class UploadService:
    def __init__(self, repository: IRepository):
        self.repository = repository

    def upload_fuzz_Target(self, file: FileStorage) -> bool:
        path = Path(current_app.config['UPLOAD_FOLDER']) / file.filename
        return self.repository.save(file, path)
