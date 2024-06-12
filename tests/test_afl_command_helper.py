from unittest.mock import MagicMock, patch
import app.helper.afl_command_helper as afl_command_helper
import pytest


def test_is_target_running_false():
    # Arrange
    target_name = "test"
    # Act
    result = afl_command_helper.is_target_running(target_name)
    # Assert
    assert result == False


def test_is_target_running_with_no_error():
    # Arrange
    with patch("subprocess.Popen") as mock_popen:
        mock_process = MagicMock()
        mock_process.communicate.return_value = ("Fuzzers alive : 1", "")
        mock_popen.return_value = mock_process

        # Act
        result = afl_command_helper.is_target_running("target_name")

        # Assert
        assert result is True


def test_stop_target_failure():
    # Arrange
    with patch("app.helper.afl_command_helper.kill_tmux_session") as mock_kill_tmux_session:
        mock_kill_tmux_session.side_effect = Exception("Error stopping target")

        # Act
        result = afl_command_helper.stop_target()

        # Assert
        assert result is False


def test_stop_target():
    # Arrange
    with patch("app.helper.afl_command_helper.kill_tmux_session") as mock_kill_tmux_session:
        with patch("app.helper.afl_command_helper.kill_ttyd") as mock_kill_ttyd:

            # Act
            result = afl_command_helper.stop_target()

            # Assert
            assert result is True


def test_delete_target_success():
    # Arrange
    target_name = "test_target"
    with patch("app.helper.afl_command_helper.is_target_running") as mock_is_target_running, \
            patch("subprocess.run") as mock_subprocess_run:
        mock_is_target_running.return_value = False
        # Act
        result = afl_command_helper.delete_target(target_name)
        # Assert
        assert result is True
        mock_is_target_running.assert_called_once_with(target_name)
        mock_subprocess_run.assert_called_with(
            ["rm", "-rf", f"fuzz_targets/{target_name}"], stdout=-1, stderr=-1, text=True)


def test_plot_fuzz_imgs():
    # Arrange
    target_name = "test_target"
    with patch("subprocess.run") as mock_subprocess_run, \
            patch("pathlib.Path.mkdir"):
        # Act
        afl_command_helper.plot_fuzz_imgs(target_name)
        # Assert
        mock_subprocess_run.assert_called_once_with(
            ["AFLplusplus/afl-plot", f"fuzz_targets/{target_name}/output/default", f"app/static/fuzz_targets_img/{target_name}"], stdout=-1, stderr=-1, text=True)


def test_kill_ttyd():
    # Arrange
    with patch("subprocess.run"):
        with patch("shlex.split") as mock_shlex_split:

            # Act
            afl_command_helper.kill_ttyd()

            # Assert
            mock_shlex_split.assert_called_once_with("pkill -f ttyd/ttyd")


def test_kill_tmux_session():
    # Arrange
    with patch("shlex.split") as mock_shlex_split, patch("subprocess.run") as mock_subprocess_run:
        mock_shlex_split.return_value = [
            "tmux", "kill-session", "-t", "AFLGUITool_session"]

        # Act
        afl_command_helper.kill_tmux_session()

        # Assert
        mock_shlex_split.assert_called_once_with(
            "tmux kill-session -t AFLGUITool_session")
        mock_subprocess_run.assert_called_once_with(
            ["tmux", "kill-session", "-t", "AFLGUITool_session"], stdout=-1, stderr=-1, text=True)
