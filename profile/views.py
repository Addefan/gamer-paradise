from flask import redirect, url_for, render_template, flash, request
from flask.views import MethodView
from flask_login import login_required, logout_user, current_user

from database import get_db
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
        form.email.data = current_user.user['email']
        form.name.data = current_user.user['name']
        return render_template('profile/personal.html', page='personal', form=form)

    def post(self):
        form = ChangeDataForm()
        if form.validate_on_submit():
            db = get_db()
            name = form.name.data
            user_id = current_user.user['id']
            db.update('UPDATE users SET name = %s WHERE id = %s', (name, user_id))
            current_user.user['name'] = name
            flash('Информация успешно изменена', 'success')
        return render_template('profile/personal.html', page='personal', form=form)


class DeleteAccountView(MethodView):
    decorators = [login_required]

    def get(self):
        user_id = current_user.user['id']
        logout_user()
        db = get_db()
        db.delete('DELETE FROM users WHERE id = %s', (user_id,))
        flash('Ваш аккаунт успешно удалён', 'success')
        return redirect(request.referrer)
