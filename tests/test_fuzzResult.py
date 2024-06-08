from app.models.fuzzResult import FuzzResult, Crash, FuzzData
from unittest.mock import Mock, patch
import pytest


@pytest.fixture
def fuzz_result():
    crashes = [
        Crash(id=2, num=2, signal_number=11, relative_time=100,
              execs=5, crashingInput="input", crash_path="path"),
        Crash(id=2, num=2, signal_number=11, relative_time=100,
              execs=5, crashingInput="input", crash_path="path")
    ]
    fuzz_data = [
        FuzzData(1, 11, 100, 5, 0.1, 0.2, 0.3, 0.4, 0.5),
        FuzzData(2, 22, 200, 10, 0.2, 0.3, 0.4, 0.5, 0.6)
    ]
    return FuzzResult(crashes, fuzz_data)


def test_num_crashes(fuzz_result):
    assert fuzz_result.num_crashes == 2


def test_get_crashed(fuzz_result):
    assert len(fuzz_result.get_crashed) == 2


def test_num_fuzz_data(fuzz_result):
    assert fuzz_result.num_fuzz_data == 2


def test_gen_target_report(fuzz_result):
    # Arrange
    with patch("app.models.fuzzResult.afl_command_helper.plot_fuzz_imgs") as mock:

        # Act
        fuzz_result.gen_target_report("test")

        # Assert
        mock.assert_called_once_with("test")
