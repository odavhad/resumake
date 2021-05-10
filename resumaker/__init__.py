from flask import Flask

from .settings import ENV_VAR

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return "Variable: {}".format(ENV_VAR.get('TEST', 'None'))

    return app
