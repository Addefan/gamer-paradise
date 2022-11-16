from flask import Blueprint

games = Blueprint('games', __name__, template_folder='templates')

from games import views

games.add_url_rule('', view_func=views.GamesView.as_view('index'))
games.add_url_rule('/add', view_func=views.CreateGameView.as_view('add'))
games.add_url_rule('/<int:game_id>/edit', view_func=views.EditGameView.as_view('edit'))
