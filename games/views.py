from os import path

from flask import render_template, request, current_app, redirect, url_for, flash
from flask.views import MethodView
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from auth.enums import Role
from database import get_db
from games import games
from games.forms import GameForm


def get_platforms_and_developers(db):
    platforms_list = db.select('SELECT DISTINCT platform FROM games '
                               'WHERE is_deleted = false AND in_stock > 0')
    if not isinstance(platforms_list, list):
        platforms_list = [platforms_list]
    developers_list = db.select('SELECT DISTINCT developer FROM games '
                                'WHERE is_deleted = false AND in_stock > 0')
    if not isinstance(developers_list, list):
        developers_list = [developers_list]
    return {'platforms': platforms_list, 'developers': developers_list}


def get_searched_sorted_filtered_games(db, user_id, initial_query, initial_vals=None):
    platforms = request.args.getlist('platform')
    developers = request.args.getlist('developer')
    order = request.args.get('order')
    search = request.args.get('search', '').lower()
    query = initial_query
    if initial_vals is None:
        initial_vals = []
    if platforms:
        query += ' AND platform = ANY(%s)'
        initial_vals.append(platforms)
    if developers:
        query += ' AND developer = ANY(%s)'
        initial_vals.append(developers)
    if search:
        query += (" AND (lower(title) LIKE '%%' || %s || '%%' OR "
                  "lower(description) LIKE '%%' || %s || '%%')")
        initial_vals.append(search)
        initial_vals.append(search)
    if order:
        sort_map = {'alphabet': 'title', 'cheap': 'price', 'expensive': 'price DESC',
                    'new': 'release_date DESC', 'old': 'release_date'}
        query += f' ORDER BY {sort_map.get(order, "id")}'
    games_list = db.select(query, initial_vals)
    if not isinstance(games_list, list):
        games_list = [games_list]
    return games_list


class GamesView(MethodView):
    def get(self):
        db = get_db()
        user_id = current_user.user['id'] if not current_user.is_anonymous else 0
        query = ('SELECT *, EXISTS (SELECT true FROM favorites '
                 'WHERE game_id = id AND user_id = %s) AS is_favorite '
                 'FROM games WHERE is_deleted = false AND in_stock > 0')
        vals = [user_id]
        return render_template('games/games.html', **get_platforms_and_developers(db),
                               games=get_searched_sorted_filtered_games(db, user_id, query, vals))


class CreateGameView(MethodView):
    decorators = [login_required]

    def get(self):
        if current_user.user['role'] != Role.admin:
            return redirect(url_for('.index'))
        form = GameForm()
        return render_template('games/game_form.html', form=form, action='Добавление товара')

    def post(self):
        form = GameForm()
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
                photo_filename = 'static/images/default_game.png'
            game_id = db.insert('INSERT INTO games (title, description, price, photo, platform, '
                                'developer, release_date, in_stock, is_deleted) VALUES '
                                '(%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id',
                                (title, description, price, photo_filename, platform, developer,
                                 release_date, in_stock, is_deleted), True)['id']
            return redirect(url_for('.game', game_id=game_id))
        return render_template('games/game_form.html', form=form, action='Добавление товара')


@games.route('/change_favorite')
@login_required
def change_favorite():
    db = get_db()
    user_id = current_user.user['id']
    game_id = request.args.get('game_id')
    if request.args.get('checked') == 'true':
        db.delete('DELETE FROM favorites WHERE user_id = %s AND game_id = %s', (user_id, game_id))
    else:
        db.insert('INSERT INTO favorites (user_id, game_id) VALUES (%s, %s)', (user_id, game_id))
    return {}


@games.route('/favorites')
@login_required
def favorites():
    db = get_db()
    user_id = current_user.user['id']
    query = ('SELECT *, EXISTS (SELECT true FROM carts '
             'WHERE game_id = id AND user_id = %s) AS in_cart '
             'FROM (SELECT game_id FROM favorites f WHERE user_id = %s) f '
             'JOIN games g ON g.id = f.game_id '
             'WHERE is_deleted = false AND in_stock > 0')
    vals = [user_id, user_id]
    return render_template('games/favorites.html', **get_platforms_and_developers(db),
                           games=get_searched_sorted_filtered_games(db, user_id, query, vals))


@games.route('/change_cart')
@login_required
def change_cart():
    db = get_db()
    user_id = current_user.user['id']
    game_id = request.args.get('game_id')
    if request.args.get('checked') == 'true':
        db.delete('DELETE FROM carts WHERE user_id = %s AND game_id = %s', (user_id, game_id))
    else:
        count = request.args.get('count')
        db.insert('INSERT INTO carts (user_id, game_id, quantity) VALUES (%s, %s, %s)',
                  (user_id, game_id, count))
    return {}


@games.route('/cart')
@login_required
def cart():
    db = get_db()
    user_id = current_user.user['id']
    games_list = db.select('SELECT * FROM '
                           '(SELECT game_id, quantity FROM carts c WHERE user_id = %s) c '
                           'JOIN (SELECT * FROM games WHERE is_deleted = false AND in_stock > 0) g '
                           'ON g.id = c.game_id ', (user_id,))
    if not isinstance(games_list, list):
        games_list = [games_list]
    return render_template('games/cart.html', games=games_list)


@games.route('/change_count_cart')
@login_required
def change_count_cart():
    db = get_db()
    user_id = current_user.user['id']
    game_id = request.args.get('game_id')
    count = request.args.get('count')
    db.update('UPDATE carts SET quantity = %s WHERE user_id = %s AND game_id = %s',
              (count, user_id, game_id))
    return {}


@games.route('/cart/make_order')
@login_required
def make_order():
    db = get_db()
    user_id = current_user.user['id']
    amount = db.select('SELECT sum(price * quantity) FROM '
                       '(SELECT game_id, quantity FROM carts WHERE user_id = %s) c '
                       'JOIN (SELECT * FROM games WHERE is_deleted = false AND in_stock > 0) g '
                       'ON g.id = c.game_id', (user_id,))['sum']
    order_id = db.insert('INSERT INTO orders (user_id, amount) VALUES (%s, %s) RETURNING id',
                         (user_id, amount), True)['id']
    db.insert('INSERT INTO orders_games (SELECT %s, c.game_id, quantity, price '
              'FROM (SELECT * FROM carts WHERE user_id = %s) c '
              'JOIN (SELECT id, price FROM games) g ON c.game_id = g.id)',
              (order_id, user_id))
    db.update('UPDATE games g SET in_stock = (in_stock - '
              '(SELECT quantity FROM carts WHERE user_id = %s AND game_id = g.id)) '
              'WHERE id IN (SELECT game_id FROM carts WHERE user_id = %s) AND '
              'is_deleted = false AND in_stock > 0', (user_id, user_id))
    db.delete('DELETE FROM carts WHERE user_id = %s', (user_id,))
    flash(f'Заказ #{order_id} успешно создан', 'success')
    return redirect(url_for('profile.order', order_id=order_id))


@games.route('/<int:game_id>')
def game(game_id):
    db = get_db()
    user_id = current_user.user['id'] if not current_user.is_anonymous else 0
    cur_game = db.select('SELECT *, (SELECT round(avg(score), 2) FROM reviews WHERE game_id = %s) '
                         'AS rating, EXISTS (SELECT true FROM reviews '
                         'WHERE user_id = %s AND game_id = %s) AS is_reviewed, '
                         'EXISTS (SELECT true FROM carts '
                         'WHERE game_id = id AND user_id = %s) AS in_cart,'
                         'EXISTS (SELECT true FROM favorites '
                         'WHERE game_id = id AND user_id = %s) AS in_favorites  '
                         'FROM games WHERE id = %s',
                         (game_id, user_id, game_id, user_id, user_id, game_id))
    return render_template('games/game.html', game=cur_game)


@games.route('/make_review')
@login_required
def make_review():
    db = get_db()
    user_id = current_user.user['id']
    game_id = request.args.get('game_id')
    score = request.args.get('score')
    db.insert('INSERT INTO reviews VALUES (%s, %s, %s)', (user_id, game_id, score))
    rating = db.select('SELECT round(avg(score), 2) FROM reviews WHERE game_id = %s',
                       (game_id,))['round']
    return {'rating': rating}


@games.route('/<int:game_id>/delete')
@login_required
def delete_game(game_id):
    if not current_user.user['role'] == Role.admin:
        return redirect(url_for('.index'))
    db = get_db()
    db.delete('UPDATE games SET is_deleted = true WHERE id = %s', (game_id,))
    flash('Товар успешно удалён', 'success')
    return redirect(url_for('.index'))


class EditGameView(MethodView):
    decorators = [login_required]

    def get(self, game_id):
        if not current_user.user['role'] == Role.admin:
            return redirect(url_for('.index'))
        db = get_db()
        cur_game = db.select('SELECT * FROM games WHERE id = %s', (game_id,))
        form = GameForm()
        form.title.data = cur_game['title']
        form.description.data = cur_game['description']
        form.price.data = float(cur_game['price'])
        form.platform.data = cur_game['platform']
        form.developer.data = cur_game['developer']
        form.release_date.data = cur_game['release_date']
        form.in_stock.data = int(cur_game['in_stock'])
        form.is_deleted.data = cur_game['is_deleted'] == 'true'
        form.submit.label.text = 'Обновить товар'
        return render_template('games/game_form.html', form=form, action='Изменение товара')

    def post(self, game_id):
        form = GameForm()
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
                photo_filename = 'static/images/default_game.png'
            game_id = db.update('UPDATE games SET (title, description, price, photo, platform, '
                                'developer, release_date, in_stock, is_deleted) = '
                                '(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                                'WHERE id = %s RETURNING id',
                                (title, description, price, photo_filename, platform, developer,
                                 release_date, in_stock, is_deleted, game_id), True)['id']
            return redirect(url_for('.game', game_id=game_id))
        return render_template('games/game_form.html', form=form, action='Обновление товара')

