from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route('/hello')
    def hello():
        return 'Hello, World!!!!'
    
    from .controllers import afl_controller
    app.register_blueprint(afl_controller.bp)

    return app