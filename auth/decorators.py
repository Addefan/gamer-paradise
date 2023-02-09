from flask import redirect, url_for
from flask_login import current_user


def not_login_required(func):
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('profile.index'))
        return func(*args, **kwargs)

    return wrapper
