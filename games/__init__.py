from flask import Blueprint

games = Blueprint('games', __name__, template_folder='templates')

from games import views

games.add_url_rule('/add', view_func=views.CreateGameView.as_view('add'))
