from flask import Blueprint

from extensions import lm

auth = Blueprint('auth', __name__, template_folder='templates')

from auth import views

lm.login_view = 'auth.login'
lm.login_message = 'Чтобы просмотреть эту страницу, необходимо авторизоваться'
lm.login_message_category = 'error'

auth.add_url_rule('/register', view_func=views.RegisterView.as_view('register'))
auth.add_url_rule('/login', view_func=views.LoginView.as_view('login'))
auth.add_url_rule('/logout', view_func=views.LogoutView.as_view('logout'))
