import pytest
from unittest.mock import Mock, patch
from pathlib import Path
from app.models.fuzzResult import FuzzResult
from app.models.fuzzTarget import FuzzTarget
from app.models.fuzzConfig import FuzzConfig
from app.models.crash import Crash


@pytest.fixture
def fuzz_target():
    fuzz_config = FuzzConfig(is_input_by_file=True)
    return FuzzTarget(name="test", dirPath=Path(""), fuzzResult=None, fuzzStatus=None, fuzzConfig=fuzz_config)


def test_run(fuzz_target):
    # Arrange
    with patch("app.models.fuzzTarget.afl_command_helper.run_target") as mock:
        mock.return_value = True

        # Act
        result = fuzz_target.run()

        # Assert
        assert result == True
        mock.assert_called_once_with(fuzz_target)


def test_is_running(fuzz_target):
    # Arrange
    with patch("app.models.fuzzTarget.afl_command_helper.is_target_running") as mock:
        mock.return_value = True

        # Act
        result = fuzz_target.is_running()

        # Assert
        assert result == True
        mock.assert_called_once_with("test")


def test_stop(fuzz_target):
    # Arrange
    with patch("app.models.fuzzTarget.afl_command_helper.stop_target") as mock:

        # Act
        fuzz_target.stop()

        # Assert
        mock.assert_called_once()


def test_gen_target_report(fuzz_target):
    # Arrange
    fake_fuzz_result = Mock(spec=FuzzResult)
    fuzz_target.fuzz_result = fake_fuzz_result

    # Act
    fuzz_target.gen_target_report()

    # Assert
    fake_fuzz_result.gen_target_report.assert_called_once_with("test")


def test_gen_target_report_none(fuzz_target):
    # Act
    result = fuzz_target.gen_target_report()

    # Assert
    assert result == None


def test_delete(fuzz_target):
    # Arrange
    with patch("app.models.fuzzTarget.afl_command_helper.delete_target") as mock:
        mock.return_value = True

        # Act
        result = fuzz_target.delete()

        # Assert
        assert result == True
        mock.assert_called_once_with("test")


def test_is_input_by_file(fuzz_target):
    # Act
    result = fuzz_target.is_input_by_file()

    # Assert
    assert result == True


def test_replay(fuzz_target):
    # Arrange
    with patch("app.models.fuzzTarget.afl_command_helper.replay_crash") as mock:
        fake_fuzz_result = Mock(spec=FuzzResult)
        fake_fuzz_result.get_specific_crash.return_value = Crash(id=1, signal_number=11, relative_time=100,
                                                                 execs=5, crashingInput="input", crash_path="fake_path")
        fuzz_target.fuzz_result = fake_fuzz_result
        mock.return_value = "fake_replay_content"

        # Act
        result = fuzz_target.replay(1)

        # Assert
        assert result == "fake_replay_content"
        fake_fuzz_result.get_specific_crash.assert_called_once_with(id=1)
        mock.assert_called_once_with("test", "fake_path", True)
