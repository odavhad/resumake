import os

from flask import Flask, render_template

from .settings import ENV_VAR

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY = ENV_VAR['SECRET_KEY'],
        DATABASE = os.path.join(app.instance_path, ENV_VAR['DATABASE']),
        TEMPLATES_AUTO_RELOAD = True
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return render_template('base.html')

    return app
