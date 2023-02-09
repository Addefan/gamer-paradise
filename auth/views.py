from flask import render_template, redirect, url_for, flash, request
from flask.views import MethodView
from flask_login import login_user, logout_user, current_user, login_required
from psycopg2 import errors
from psycopg2.errorcodes import UNIQUE_VIOLATION
from werkzeug.security import generate_password_hash, check_password_hash

from auth.forms import RegisterForm, LoginForm
from auth.models import User
from extensions import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class RegisterView(MethodView):
    def get(self):
        if current_user.is_authenticated:
            flash('Вы уже зарегистрированы', 'warning')
            return redirect(url_for('profile.index'))

        form = RegisterForm()
        return render_template('auth/auth.html', action='Регистрация', form=form)

    def post(self):
        form = RegisterForm()
        if form.validate_on_submit():
            User.create(email=form.email.data, password=form.password.data)
            flash('Вы успешно зарегистрированы', 'success')
            return redirect(url_for('.login'))
        return render_template('auth/auth.html', action='Регистрация', form=form)


class LoginView(MethodView):
    def get(self):
        if current_user.is_authenticated:
            flash('Вы уже авторизованы', 'warning')
            return redirect(url_for('profile.index'))

        form = LoginForm()
        return render_template('auth/auth.html', action='Авторизация', form=form)

    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            db = get_db()
            user = db.select(f'SELECT * FROM users WHERE email = %s', (email,))
            if user and check_password_hash(user['password'], password):
                user = UserLogin().get_user(db, email=email)
                login_user(user, remember)
                flash('Вы успешно авторизованы', 'success')
                return redirect(request.args.get('next') or url_for('games.index'))
            else:
                form.email.errors.append('Неверный адрес электронной почты или пароль')
                form.password.errors.append('Неверный адрес электронной почты или пароль')
        return render_template('auth/auth.html', action='Авторизация', form=form)


class LogoutView(MethodView):
    decorators = [login_required]

    def get(self):
        logout_user()
        flash('Вы успешно вышли из аккаунта', 'success')
        return redirect(request.referrer)
