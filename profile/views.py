from flask import redirect, url_for, render_template, flash, request
from flask.views import MethodView
from flask_login import login_required, current_user

from auth.models import User
from games.models import Order, OrderGame, Game
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
        form.email.data = current_user.email
        form.name.data = current_user.name
        return render_template('profile/personal.html', page='personal', form=form)

    def post(self):
        form = ChangeDataForm()
        if form.validate_on_submit():
            user = User.query.get(current_user.id)
            if user.update(name=form.name.data):
                flash('Информация успешно изменена', 'success')
            else:
                flash('Информацию изменить не удалось, попробуйте позже', 'error')
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
            games_titles = db.select('SELECT ARRAY(SELECT title FROM games g '
                                     'JOIN orders_games og on g.id = og.game_id '
                                     'WHERE order_id = %s)', (order['id'],))['array']
            orders_games_titles.append((order, games_titles))
        return render_template('profile/orders.html', page='orders',
                               orders_games_titles=orders_games_titles)


class DeleteAccountView(MethodView):
    decorators = [login_required]

    def get(self):
        user = User.query.get(current_user.id)
        if user.delete():
            flash('Ваш аккаунт успешно удалён', 'success')
        else:
            flash('Аккаунт удалить не удалось, попробуйте позже', 'error')
        return redirect(request.referrer)


class OrderView(MethodView):
    decorators = [login_required]

    def get(self, order_id):
        order = Order.query.get(order_id)
        if not order.user_id == current_user.id:
            return redirect(url_for('profile.orders'))
        games = Game.query(OrderGame).filter_by(order_id=order.id)
        return render_template('profile/order.html', page='orders', order=order, games=games)
