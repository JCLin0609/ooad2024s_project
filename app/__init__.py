from flask import Flask
from .controllers import afl_controller
import atexit
import os
from app.helper import afl_command_helper


def create_app():
    app = Flask(__name__)
    app.register_blueprint(afl_controller.bp)
    # 配置文件上傳的文件夾位置和文件大小限制
    app.config['UPLOAD_FOLDER'] = 'fuzz_targets/'
    app.config['TARGET_IMG_FOLDER'] = 'app/static/fuzz_targets_img/'
    app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024  # 限制16MB
    app.secret_key = os.urandom(12).hex()
    atexit.register(afl_command_helper.kill_tmux_session)
    atexit.register(afl_command_helper.kill_ttyd)

    return app
