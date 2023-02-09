import os
from datetime import datetime

from auth.models import User
from database import db, CRUDMixin


class Game(CRUDMixin, db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(14, 2), nullable=False, default=0)
    photo = db.Column(db.String(127), nullable=False, default=os.path.join('static', 'images', 'default_game.png'))
    platform = db.Column(db.String(20), nullable=False)
    developer = db.Column(db.String(127), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    in_stock = db.Column(db.Integer, default=0)
    is_deleted = db.Column(db.Boolean(), default=False)


class UserGameBaseModel(CRUDMixin, db.Model):
    __abstract__ = True

    user_id = db.Column(db.ForeignKey(User.id), primary_key=True, onupdate="CASCADE", ondelete="CASCADE")
    game_id = db.Column(db.ForeignKey(Game.id), primary_key=True, onupdate="CASCADE", ondelete="CASCADE")


class Favorite(UserGameBaseModel):
    pass


class Cart(UserGameBaseModel):
    quantity = db.Column(db.Integer)


class Review(UserGameBaseModel):
    score = db.Column(db.SmallInteger)


class Order(CRUDMixin, db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.ForeignKey(User.id), onupdate="CASCADE", ondelete="SET NULL")
    date = db.Column(db.DateTime(timezone=True), default=datetime.now())
    amount = db.Column(db.Numeric(14, 2), nullable=False)


class OrderGame(CRUDMixin, db.Model):
    order_id = db.Column(db.ForeignKey(Order.id), primary_key=True, onupdate="CASCADE", ondelete="CASCADE")
    game_id = db.Column(db.ForeignKey(Game.id), primary_key=True, onupdate="CASCADE", ondelete="SET NULL")
    quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric(14, 2), nullable=False)
