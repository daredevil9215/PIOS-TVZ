from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                 unique=False)
    lastname: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=False)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=False)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    is_admin = db.Column(db.Boolean(), default=False)
    balance = db.Column(db.Float, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    user_orders = db.relationship(
        'Order', backref='order', cascade='all, delete-orphan')

    @login.user_loader
    def load_user(id):
        return db.session.get(User, int(id))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=True)
    name = db.Column(db.String(100), nullable=True)
    route = db.Column(db.String(100), nullable=True)
    total_seats = db.Column(db.Integer, nullable=False, default=0)
    reserved_seats = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Float, nullable=False)
    order_tickets = db.relationship(
        'OrderTicket', backref='ticket', overlaps="orders,ticket")
    # cart_items = db.relationship('CartItem', backref='ticket', lazy=True)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(
        db.String(20), nullable=False)

    order_tickets = db.relationship(
        'OrderTicket', backref='order', cascade='all, delete-orphan', overlaps="orders,ticket")
    user = db.relationship(
        'User'
    )


class OrderTicket(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey(
        'order.id'), primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey(
        'ticket.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    __table_args__ = (
        db.PrimaryKeyConstraint('order_id', 'ticket_id'),
    )


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=True)  # Nullable for guest cart items
    ticket_id = db.Column(db.Integer, db.ForeignKey(
        'ticket.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
