from app.models.crash import Crash


def test_crash_get_data():
    crash = Crash(id=1, signal_number=11, relative_time=100,
                  execs=5, crashingInput="input", crash_path="path")
    expected_data = {
        "id": 1,
        "signal_number": 11,
        "relative_time": 100,
        "execs": 5,
        "crashingInput": "input"
    }
    assert crash.get_data == expected_data
