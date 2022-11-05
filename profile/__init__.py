from flask import Blueprint

profile = Blueprint('profile', __name__, template_folder='templates')

from profile import views
