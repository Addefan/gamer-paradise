from flask import Blueprint

games = Blueprint('games', __name__, template_folder='templates')

from games import views
