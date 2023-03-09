from http import HTTPStatus

from flask import Flask, render_template

import filters
from auth import auth
from commands import create_db, drop_db
from config import Config
from database import db
from extensions import bootstrap, login_manager
from games import games
from profile import profile


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)
    register_filters(app)
    register_errorhandlers(app)
    register_commands(app)

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
    app.register_blueprint(games, url_prefix='/games')


def register_filters(app):
    app.add_template_filter(filters.date, 'date')
    app.add_template_filter(filters.cart_amount, 'cart_amount')
    app.add_template_filter(filters.difference, 'difference')


def register_errorhandlers(app):
    def render_error(e):
        print(e)
        return render_template('%s.html' % e.code), e.code

    for e in [
        HTTPStatus.NOT_FOUND,
        HTTPStatus.INTERNAL_SERVER_ERROR,
    ]:
        app.register_error_handler(e, render_error)


def register_commands(app):
    for command in (create_db, drop_db):
        app.cli.add_command(command)


if __name__ == "__main__":
    create_app().run(debug=True)
