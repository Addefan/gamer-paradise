from flask import redirect, url_for, render_template, flash, request
from flask.views import MethodView
from flask_login import login_required, current_user

from auth.models import User
from games.models import Order
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
        orders = Order.query.filter_by(user_id=current_user.id)
        orders_games_titles = []
        for order in orders:
            games_titles = (order_game.game.title for order_game in order.games)
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
        order_games = order.games
        return render_template('profile/order.html', page='orders', order=order, order_games=order_games)
