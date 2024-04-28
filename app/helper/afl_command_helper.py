import os
from pathlib import Path
import shlex
import subprocess


afl_path = Path("./AFLplusplus/afl-fuzz")
afl_whatsup_path = Path("./AFLplusplus/afl-whatsup")
afl_plot_path = Path("./AFLplusplus/afl-plot")
ttyd_path = Path("./ttyd/ttyd")
ttyd_port = 5001
fuzz_targets_path = Path("./fuzz_targets")
fuzz_targets_img_path = Path("./app/static/fuzz_targets_img")
tmux_session_name = "AFLGUITool_session"


def is_target_running(target_name: str) -> bool:
    output_path = fuzz_targets_path / target_name / "output"
    command = f"{afl_whatsup_path} {output_path}"
    process = subprocess.Popen(
        shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = process.communicate()
    if error:
        print(f"Error checking if target is running: {error}")
        return False
    return "Fuzzers alive : 0" not in output


def run_target(target_name: str):
    try:
        stop_target()
        env = os.environ.copy()
        env['AFL_AUTORESUME'] = '1'
        env['AFL_I_DONT_CARE_ABOUT_MISSING_CRASHES'] = '1'
        target_path = fuzz_targets_path / target_name
        binary_path = target_path / target_name
        if not target_path.exists() or not binary_path.exists():
            return False
        command = (["tmux", "new-session", "-d", "-A", "-s", f"{tmux_session_name}", f"{afl_path}", "-i", f"{target_path}/input",
                    "-o", f"{target_path}/output", f"{binary_path}"])
        subprocess.Popen(command, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, env=env)

        ttyd_command = f"{ttyd_path} -p {ttyd_port} tmux attach -t {tmux_session_name}"
        subprocess.Popen(shlex.split(ttyd_command),
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return True
    except Exception as e:
        stop_target()
        print(f"Error running target: {e}")
        return False


def stop_target():
    try:
        kill_tmux_session()
        kill_ttyd()
        return True
    except Exception as e:
        print(f"Error stopping target: {e}")
        return False


def plot_fuzz_imgs(target_name: str) -> None:
    try:
        target_path = fuzz_targets_path / target_name / "output" / "default"
        output_path = fuzz_targets_img_path / target_name
        command = f"{afl_plot_path} {target_path} {output_path}"
        subprocess.run(shlex.split(command), stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, text=True)
    except Exception as e:
        print(f"Error plotting fuzz data: {e}")


def kill_ttyd(signum=None, frame=None):
    command = f"pkill -f {ttyd_path}"
    subprocess.run(shlex.split(command), stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE, text=True)


def kill_tmux_session(signum=None, frame=None):
    command = f"tmux kill-session -t {tmux_session_name}"
    subprocess.run(shlex.split(command), stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE, text=True)
