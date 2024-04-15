from flask import Flask
import os


def create_app():
    app = Flask(__name__)

    from .controllers import afl_controller
    app.register_blueprint(afl_controller.bp)

    app.secret_key = os.urandom(12).hex()
    
    # 配置文件上傳的文件夾位置和文件大小限制
    app.config['UPLOAD_FOLDER'] = 'fuzz_targets/'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制16MB

    return app
