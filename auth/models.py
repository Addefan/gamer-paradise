from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from auth.enums import Role
from database import db, CRUDMixin


class User(CRUDMixin, UserMixin, db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String(320), nullable=False, unique=True)
    password = db.Column(db.String(127), nullable=False)
    name = db.Column(db.String(255))
    role = db.Column(db.Enum(Role), default=Role.user)

    def __init__(self, password, **kwargs):
        super().__init__(**kwargs)
        self.set_password(password)

    @property
    def is_admin(self):
        return self.user.role == Role.admin

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
