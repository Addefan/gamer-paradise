from flask import Blueprint

profile = Blueprint('profile', __name__, template_folder='templates')

from profile import views

profile.add_url_rule('/delete', view_func=views.DeleteAccountView.as_view('delete'))
