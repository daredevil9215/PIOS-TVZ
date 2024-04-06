from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """
    User database model.

    Attributes
    ----------
    id : int, primary key
        User ID.

    firstname : string
        User's first name.

    lastname : string
        User's last name.

    email : string
        User's email address.

    password_hash : string
        User's hashed password.

    is_admin : bool
        User's administrator rights, default=False

    balance : float
        User's account balance in euros, default = 0.0
    """
    id = db.Column(db.Integer, primary_key=True)
    firstname: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                 unique=False)
    lastname: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=False)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    is_admin = db.Column(db.Boolean(), default=False)
    balance = db.Column(db.Float, nullable=False)

    @login.user_loader
    def load_user(id):
        """
        Method for loading the user object from the database.

        Parameters
        ----------
        id : int
            User ID.

        Returns
        -------
        database_result : database_object | None
        """
        return db.session.get(User, int(id))

    def set_password(self, password):
        """
        Method for generating a password hash.

        Parameters
        ----------
        password : string
            Password for hashing.

        Returns
        -------
        None
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Method for verifying a password hash.

        Parameters
        ----------
        password : string
            Password for verification.

        Returns
        -------
        verification_result : bool
        """

        return check_password_hash(self.password_hash, password)


class Ticket(db.Model):
    """
    Ticket database model.

    Attributes
    ----------
    id : int, primary key
        Ticket ID.

    city : string
        City in which the ticket is applicable.

    name : string
        Name of the public transport route the ticket applies to.

    route : string
        Endpoints of the route.

    total_seats : int
        Total number of seats in the public transport vehicle.

    reserved_seats : int
        Number of reserved seats in the public transport vehicle.

    price : float
        Ticket price.
    """
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
    """
    Order database model.

    Attributes
    ----------
    id : int, primary key
        Order ID.

    user_id : int
        ID of the user who is the order owner.

    total_amount : float
        Order amount in euros.

    payment_method : string
        Payment method selected, available options are gotovina (cash) and kartica (credit card).
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(
        db.String(20), nullable=False)

    user = db.relationship('User', backref='orders')
    order_tickets = db.relationship(
        'OrderTicket', backref='order', cascade='all, delete-orphan', overlaps="orders,ticket")


class OrderTicket(db.Model):
    """
    OrderTicket database model.

    Attributes
    ----------
    order_id : int, primary key
        Order ID.

    ticket_id : int, primary key
        Ticket ID.

    quantity : int
        Quantity of tickets to purchase.
    """
    order_id = db.Column(db.Integer, db.ForeignKey(
        'order.id'), primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey(
        'ticket.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    __table_args__ = (
        db.PrimaryKeyConstraint('order_id', 'ticket_id'),
    )


class CartItem(db.Model):
    """
    CartItem database model.

    Attributes
    ----------
    id : int, primary key
        Cart_Item ID.

    user_id : int
        ID of the user who is the cart item owner.

    ticket_id : int
        Ticket ID.

    quantity : int
        Quantity of tickets to purchase.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=True)  # Nullable for guest cart items
    ticket_id = db.Column(db.Integer, db.ForeignKey(
        'ticket.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
