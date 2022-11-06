from flask import redirect, url_for, flash, request
from flask.views import MethodView
from flask_login import login_required, logout_user, current_user

from database import get_db
from profile import profile


@profile.route('/')
@login_required
def index():
    return redirect(url_for('.personal'))


class DeleteAccountView(MethodView):
    decorators = [login_required]

    def get(self):
        user_id = current_user.user['id']
        logout_user()
        db = get_db()
        db.delete('DELETE FROM users WHERE id = %s', (user_id,))
        flash('Ваш аккаунт успешно удалён', 'success')
        return redirect(request.referrer)
