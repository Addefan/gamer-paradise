from os import path

from flask import render_template, request, current_app, redirect, url_for
from flask.views import MethodView
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from auth.enums import Role
from database import get_db
from games.forms import CreateGameForm


class GamesView(MethodView):
    def get(self):
        db = get_db()
        user_id = current_user.user['id'] if not current_user.is_anonymous else 0
        platforms = request.args.getlist('platform')
        query = ('SELECT *, EXISTS (SELECT true FROM favorites '
                 'WHERE game_id = id AND user_id = %s) AS is_favorite '
                 'FROM games WHERE is_deleted = false')
        vals = [user_id]
        if platforms:
            query += ' AND platform = ANY(%s)'
            vals += [platforms]
        games = db.select(query, vals)
        return render_template('games/games.html', games=games)


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
