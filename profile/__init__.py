from flask import Blueprint

profile = Blueprint('profile', __name__, template_folder='templates')

from profile import views

profile.add_url_rule('/personal', view_func=views.PersonalView.as_view('personal'))
profile.add_url_rule('/delete', view_func=views.DeleteAccountView.as_view('delete'))
