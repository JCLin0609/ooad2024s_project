import pytest
from pathlib import Path
from werkzeug.datastructures import FileStorage
from app.services.upload_service import UploadService
from app.Repository.IRepository import IRepository
from unittest.mock import Mock, patch
from flask import Flask


@pytest.fixture
def repository():
    return Mock(spec=IRepository)


def test_upload_fuzz_Target(repository):
    # Arrange
    app = Flask('test')
    with app.app_context():
        with patch("app.services.upload_service.current_app.config", {"UPLOAD_FOLDER": "uploads"}):
            file = FileStorage(filename='test.txt')
            repository.save.return_value = True
            upload_service = UploadService(repository=repository)
            
            # Act
            result = upload_service.upload_fuzz_Target(
                file, is_input_by_file=True)
            
            # Assert
            assert result == True
            repository.save.assert_called_once_with(
                file, Path("uploads/test.txt"), '{\n    "isInputByFile": true\n}')
