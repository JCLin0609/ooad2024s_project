from unittest.mock import Mock
from app.Repository.IRepository import IRepository
from app.models.fuzzTarget import FuzzTarget
from app.services.afl_service import AFLService


def test_current_running_target_none():
    # Arrange
    repository_mock = Mock()
    repository_mock.get_all.return_value = []
    service = AFLService(repository_mock)

    # Act
    result = service.current_running_target()

    # Assert
    assert result == None
    repository_mock.get_all.assert_called_once()


def test_current_running_target():
    # Arrange
    fuzz_target_mock = Mock(FuzzTarget)
    fuzz_target_mock.is_running.return_value = True
    targets = [fuzz_target_mock]
    repository_mock = Mock()
    repository_mock.get_all.return_value = targets
    service = AFLService(repository_mock)

    # Act
    result = service.current_running_target()

    # Assert
    assert result == fuzz_target_mock
    repository_mock.get_all.assert_called_once()


def test_current_running_target_name_none():
    # Arrange
    repository_mock = Mock()
    repository_mock.get_all.return_value = []
    service = AFLService(repository=repository_mock)

    # Act
    result = service.current_running_target_name()

    # Assert
    assert result == None


def test_currrent_running_target_name():
    # Arrange
    fuzz_target_mock = Mock(FuzzTarget)
    fuzz_target_mock.is_running.return_value = True
    fuzz_target_mock.name = "test"
    targets = [fuzz_target_mock]
    repository_mock = Mock()
    repository_mock.get_all.return_value = targets
    service = AFLService(repository_mock)

    # Act
    result = service.current_running_target_name()

    # Assert
    assert result == "test"
    repository_mock.get_all.assert_called_once()


def test_start_running_target():
    # Arrange
    fuzz_target_mock = Mock(FuzzTarget)
    fuzz_target_mock.name = "test"
    fuzz_target_mock.run.return_value = True
    repository_mock = Mock()
    repository_mock.get.return_value = fuzz_target_mock
    service = AFLService(repository_mock)

    # Act
    result = service.start_running_target("test")

    # Assert
    repository_mock.get.assert_called_once_with("test")
    fuzz_target_mock.run.assert_called_once()
    assert result is True


def test_start_running_target_none():
    # Arrange
    repository_mock = Mock()
    repository_mock.get.return_value = None
    service = AFLService(repository_mock)

    # Act
    result = service.start_running_target("not_exist")

    # Assert
    repository_mock.get.assert_called_once_with("not_exist")
    assert result is False


def test_start_running_target_with_exception():
    # Arrange
    repository_mock = Mock()
    repository_mock.get.side_effect = Exception()
    service = AFLService(repository_mock)

    # Act
    result = service.start_running_target("exception")

    # Assert
    repository_mock.get.assert_called_once_with("exception")
    assert result is False


def test_stop_running_target_none():
    # Arrange
    repository_mock = Mock()
    repository_mock.get_all.return_value = []
    service = AFLService(repository_mock)

    # Act
    result = service.stop_running_target()

    # Assert
    assert result is False


def test_stop_running_target():
    # Arrange
    fuzz_target_mock = Mock(FuzzTarget)
    fuzz_target_mock.is_running.return_value = True
    repository_mock = Mock()
    repository_mock.get_all.return_value = [fuzz_target_mock]
    service = AFLService(repository_mock)

    # Act
    result = service.stop_running_target()

    # Assert
    fuzz_target_mock.stop.assert_called_once()
    assert result is True


def test_delete_target():
    # Arrange
    fuzz_target_mock = Mock(FuzzTarget)
    fuzz_target_mock.name = "test"
    fuzz_target_mock.delete.return_value = True
    repository_mock = Mock()
    repository_mock.get.return_value = fuzz_target_mock
    service = AFLService(repository_mock)

    # Act
    result = service.delete_target(["test"])

    # Assert
    repository_mock.get.assert_called_once_with("test")
    fuzz_target_mock.delete.assert_called_once()
    assert result is True


def test_delete_target_none():
    # Arrange
    repository_mock = Mock()
    repository_mock.get.return_value = None
    service = AFLService(repository_mock)

    # Act
    result = service.delete_target(["not_exist"])

    # Assert
    repository_mock.get.assert_called_once_with("not_exist")
    assert result is False
