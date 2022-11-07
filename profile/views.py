from flask import redirect, url_for, render_template, flash, request
from flask.views import MethodView
from flask_login import login_required, logout_user, current_user

from database import get_db, db_dict_to_list
from profile import profile
from profile.forms import ChangeDataForm


@profile.route('/')
@login_required
def index():
    return redirect(url_for('.personal'))


class PersonalView(MethodView):
    decorators = [login_required]

    def get(self):
        form = ChangeDataForm()
        form.email.data = current_user.user['email']
        form.name.data = current_user.user['name']
        return render_template('profile/personal.html', page='personal', form=form)

    def post(self):
        form = ChangeDataForm()
        if form.validate_on_submit():
            db = get_db()
            name = form.name.data
            user_id = current_user.user['id']
            db.update('UPDATE users SET name = %s WHERE id = %s', (name, user_id))
            current_user.user['name'] = name
            flash('Информация успешно изменена', 'success')
        return render_template('profile/personal.html', page='personal', form=form)


class OrdersView(MethodView):
    decorators = [login_required]

    def get(self):
        db = get_db()
        user_id = current_user.user['id']
        orders = db.select('SELECT * FROM orders WHERE user_id = %s', (user_id,))
        if not isinstance(orders, list):
            orders = [orders]
        orders_games_titles = []
        for order in orders:
            games_ids = [db_dict_to_list('game_id', db.select('SELECT game_id FROM orders_games '
                                                              'WHERE order_id = %s',
                                                              (order['id'],)))]
            games_titles = db_dict_to_list('title', db.select('SELECT title FROM games '
                                                              'WHERE id = ANY(%s)',
                                                              (games_ids, )))
            orders_games_titles.append((order, games_titles))
        return render_template('profile/orders.html', page='orders',
                               orders_games_titles=orders_games_titles)


class DeleteAccountView(MethodView):
    decorators = [login_required]

    def get(self):
        user_id = current_user.user['id']
        logout_user()
        db = get_db()
        db.delete('DELETE FROM users WHERE id = %s', (user_id,))
        flash('Ваш аккаунт успешно удалён', 'success')
        return redirect(request.referrer)


class OrderView(MethodView):
    decorators = [login_required]

    def get(self, order_id):
        db = get_db()
        order = db.select('SELECT * FROM orders WHERE id = %s', (order_id,))
        if not order['user_id'] == current_user.user['id']:
            return redirect(url_for('profile.orders'))
        games = db.select('SELECT game_id, title, photo, og.price, quantity FROM orders_games og '
                          'JOIN games g ON og.game_id = g.id WHERE order_id = %s', (order_id,))
        if not isinstance(games, list):
            games = [games]
        return render_template('profile/order.html', page='orders', order=order, games=games)
