from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route('/hello')
    def hello():
        return 'Hello, World!!!!'
    
    from .controllers import afl_controller
    app.register_blueprint(afl_controller.bp)

    # 配置文件上傳的文件夾位置和文件大小限制
    app.config['UPLOAD_FOLDER'] = 'uploads/'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制16MB
    
    return app