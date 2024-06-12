from app.Repository.fuzz_target_repository import FuzzTargetRepository
from flask import Flask
from unittest.mock import Mock, patch
from werkzeug.datastructures import FileStorage
import pytest


@pytest.fixture
def repository(tmp_path):
    app = Flask('test')
    with app.app_context():
        with patch('app.Repository.fuzz_target_repository.current_app') as mock_app:
            mock_app.config = {
                'UPLOAD_FOLDER': tmp_path / 'uploads',
                'TARGET_IMG_FOLDER': tmp_path / 'target_imgs'
            }
            yield FuzzTargetRepository()


def test_save(repository, tmp_path):
    # Arrange
    file_mock = Mock(spec=FileStorage, wraps=FileStorage())
    file_mock.filename = 'test_file.txt'
    tmp_path = tmp_path / 'test'

    # Act
    result = repository.save(file_mock, tmp_path, '{"config": "test"}')

    # Assert
    assert result is True
    file_mock.save.assert_called_once_with(tmp_path / 'test_file.txt')
    (tmp_path / 'test_file.txt').exists()
    (tmp_path / 'input' / 'seed.txt').exists()
    (tmp_path / 'config.json').exists()


def test_save_false(repository):
    # Arrange
    file = None
    path = None
    config_json = None

    # Act
    result = repository.save(file, path, config_json)

    # Assert
    assert result == False


def test_save_file_with_exception(repository, tmp_path):
    # Arrange
    file = Mock(spec=FileStorage)
    file.filename = 'test_file.txt'
    config_json = '{"config": "test"}'

    # Act
    result = repository.save(file, tmp_path / 'test', config_json)

    # Assert
    assert result == False


def test_get_existing_target(repository, tmp_path):
    target_name = 'test_target'
    target_dir = tmp_path / 'uploads'
    target_path = target_dir / target_name
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path.touch()  # Create an empty file to simulate the target's existence

    # Mock the internal methods
    with patch.object(repository, '_FuzzTargetRepository__get_fuzz_result_by_name', return_value='result') as mock_get_fuzz_result, \
            patch.object(repository, '_FuzzTargetRepository__get_fuzz_status_by_name', return_value='status') as mock_get_fuzz_status, \
            patch.object(repository, '_FuzzTargetRepository__get_fuzz_config_by_name', return_value='config') as mock_get_fuzz_config:

        target = repository.get(target_name)

        assert target is not None
        assert target.name == target_name
        assert target.dir_path == target_path
        assert target.fuzz_result == 'result'
        assert target.fuzz_status == 'status'
        assert target.fuzz_config == 'config'

        mock_get_fuzz_result.assert_called_once_with(target_name)
        mock_get_fuzz_status.assert_called_once_with(target_name)
        mock_get_fuzz_config.assert_called_once_with(target_name)
