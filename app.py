from flask import Flask, render_template

import database as db
from auth import auth
from config import Config

from extensions import bootstrap, login_manager
from profile import profile


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app


def register_extensions(app):
    bootstrap.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)


def register_blueprints(app):
    app.register_blueprint(auth)
    app.register_blueprint(profile, url_prefix='/profile')


if __name__ == "__main__":
    create_app().run(debug=True)
