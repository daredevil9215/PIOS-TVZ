from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField, BooleanField, RadioField, PasswordField, SelectField, FieldList, FormField
from wtforms.validators import ValidationError, DataRequired, EqualTo, NumberRange, Optional, Email
import sqlalchemy as sa
from app import db
from app.models import User, Order, OrderTicket


class TicketForm(FlaskForm):
    name = StringField('Ime', validators=[
        DataRequired(message="Ime je obavezno.")])
    city = StringField('Grad', validators=[
        DataRequired(message="Grad je obavezan.")])
    price = FloatField('Cijena', validators=[
        DataRequired(message="Cijena je obavezna.")
    ])
    route = StringField('Linija',
                        validators=[])
    total_seats = IntegerField('Ukupno Mjesta', validators=[])
    submit = SubmitField('Spremi Promjene')


class UserForm(FlaskForm):
    firstname = StringField('Ime', validators=[
        DataRequired(message="Ime je obavezno.")])
    lastname = StringField('Prezime', validators=[
                           DataRequired(message="Prezime je obavezno.")])
    username = StringField('Korisničko ime', validators=[
                           DataRequired(message="Korisničko ime je obavezno.")])
    password = PasswordField('Lozinka', validators=[
                             DataRequired("Lozinka je obavezna.")])
    password2 = PasswordField(
        'Ponovi Lozinku', validators=[DataRequired("Lozinka je obavezna."), EqualTo('password')]
    )
    email = StringField('Email', validators=[DataRequired(), Email()])
    balance = FloatField('Stanje računa',
                         validators=[DataRequired(message="Stanje računa je obavezno."),
                                     NumberRange(min=0, max=float('inf'), message='Stanje računa ne smije biti negativno.')])
    is_admin = RadioField(
        'Admin', choices=[(True, 'Da'), (False, 'Ne')], coerce=bool, default=False)
    submit = SubmitField('Spremi')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.original_username = kwargs.get(
            'obj').username if kwargs.get('obj') else None

    def validate_username(self, field):
        if field.data == self.original_username:
            return  # Skip validation if username is not changed

        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('Molimo koristite drugo korisničko ime.')


class OrderedTicketForm(FlaskForm):
    ticket_name = StringField('Ticket Name', render_kw={'readonly': True})
    quantity = IntegerField('Quantity', validators=[
                            DataRequired(), NumberRange(min=1)])


class EditOrderForm(FlaskForm):
    payment_method = SelectField('Payment Method', choices=[(
        'gotovina', 'Gotovina'), ('kartica', 'Kartica')], validators=[DataRequired()])
    ordered_tickets = FieldList(FormField(OrderedTicketForm), min_entries=1)
    submit = SubmitField('Update')

    def populate_from_model(self, order):
        self.payment_method.data = order.payment_method
        for ordered_ticket in order.order_tickets:
            form = OrderedTicketForm()
            form.ticket_name.data = ordered_ticket.ticket.name
            form.quantity.data = ordered_ticket.quantity
            self.ordered_tickets.append_entry(form)
