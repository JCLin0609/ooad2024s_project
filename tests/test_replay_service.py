from app.services.replay_service import ReplayService
import pytest
from unittest.mock import Mock
from app.Repository.IRepository import IRepository


@pytest.fixture
def repository():
    return Mock(spec=IRepository)


def test_replay_target(repository):
    # Arrange
    replay_service = ReplayService(repository)
    target_name = "test"
    crash_id = 1

    # Act
    replay_service.replay_target(target_name, crash_id)

    # Assert
    repository.get.assert_called_once_with(target_name)
    repository.get.return_value.replay.assert_called_once_with(crash_id)
