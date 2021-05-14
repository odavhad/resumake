import os

from flask import Flask, redirect, render_template, session, url_for

from .settings import ENV_VAR


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=ENV_VAR['SECRET_KEY'],
        DATABASE=os.path.join(app.instance_path, ENV_VAR['DATABASE']),
        TEMPLATES_AUTO_RELOAD=True
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from .routes.view import view_bp
    app.register_blueprint(view_bp)

    from .routes.add import add_bp
    app.register_blueprint(add_bp)

    from .routes.remove import remove_bp
    app.register_blueprint(remove_bp)

    @app.route('/')
    def index():
        if session.get('user_id') is not None:
            return redirect(url_for('view.general'))

        return render_template('home.html')

    return app
