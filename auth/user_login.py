from flask_login import UserMixin


class UserLogin(UserMixin):
    def __init__(self):
        self.user = None

    def get_id(self):
        return str(self.user['id'])

    def get_user(self, db, user_id=None, email=None):
        if user_id is None:
            self.user = db.select(f"SELECT * FROM users WHERE email = '%s'", (email,))
        elif email is None:
            self.user = db.select(f'SELECT * FROM users WHERE id = %s', (user_id,))
        return self

    def set_user(self, user):
        self.user = user
        return self
