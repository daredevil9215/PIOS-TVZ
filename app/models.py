from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from flask_login import UserMixin

#class User(db.Model):
#    id: so.Mapped[int] = so.mapped_column(primary_key=True)
#    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
#                                                unique=True)
#    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
#                                             unique=True)
#    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
#    role: so.Mapped[str] = so.mapped_column(sa.String(10), index=True, unique=True)
#
#    def __repr__(self):
#        return '<User {}>'.format(self.username)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    role = db.Column(db.String(20), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True)
    basket_items = db.relationship('BasketItem', backref='user', lazy=True)

    @login.user_loader
    def load_user(id):
        return db.session.get(User, int(id))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    #quantity = db.Column(db.Integer, default=1, nullable=False)
    orders = db.relationship('Order', secondary='order_ticket', backref='tickets', lazy=True)
    basket_items = db.relationship('BasketItem', backref='ticket', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)

class OrderTicket(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), primary_key=True)

class BasketItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

#class Notification(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#    message = db.Column(db.Text, nullable=False)
