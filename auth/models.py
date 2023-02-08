from flask_login import UserMixin

from auth.enums import Role
from database import db


class User(UserMixin, db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String(320), nullable=False, unique=True)
    password = db.Column(db.String(127), nullable=False)
    name = db.Column(db.String(255))
    role = db.Column(db.Enum(Role), default=Role.user)
