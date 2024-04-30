from app.models.fuzzResult import FuzzResult, Crash, FuzzData
import pytest

@pytest.fixture
def fuzz_result():
    crashes = [
        Crash(1, 11, 100, 5, "input1"),
        Crash(2, 22, 200, 10, "input2")
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
