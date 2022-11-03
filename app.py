from flask import Flask, render_template

import database as db
from auth import auth
from config import Config

from extensions import bootstrap, lm


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)

    @app.route('/')
    def main():
        return render_template('base.html')

    return app


def register_extensions(app):
    bootstrap.init_app(app)
    lm.init_app(app)
    db.init_app(app)


def register_blueprints(app):
    app.register_blueprint(auth)


if __name__ == "__main__":
    create_app().run(debug=True)
