from os import path

from flask import render_template, request, current_app, redirect, url_for
from flask.views import MethodView
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from auth.enums import Role
from database import get_db
from games.forms import CreateGameForm


class CreateGameView(MethodView):
    decorators = [login_required]

    def get(self):
        if current_user.user['role'] != Role.admin:
            return redirect(url_for('.index'))
        form = CreateGameForm()
        return render_template('games/create_game.html', form=form)

    def post(self):
        form = CreateGameForm()
        if form.validate_on_submit():
            title = form.title.data
            description = form.description.data
            price = form.price.data
            photo = form.photo.data
            platform = form.platform.data
            developer = form.developer.data
            release_date = form.release_date.data
            in_stock = form.in_stock.data
            is_deleted = form.is_deleted.data
            db = get_db()
            if photo:
                photo_filename = path.join('static', 'images', secure_filename(photo.filename))
                photo.save(path.join(path.dirname(current_app.instance_path), photo_filename))
            else:
                photo_filename = '/static/images/default_game.png'
            db.insert('INSERT INTO games (title, description, price, photo, platform, developer, '
                      'release_date, in_stock, is_deleted) VALUES '
                      '(%s, %s, %s, %s, %s, %s, %s, %s, %s) ',
                      (title, description, price, photo_filename, platform, developer, release_date,
                       in_stock, is_deleted))
            return redirect(url_for('.index'))  # TODO: поменять на URL созданного товара
        return render_template('games/create_game.html', form=form)
