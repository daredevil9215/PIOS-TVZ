from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField
from wtforms.validators import ValidationError, DataRequired, EqualTo, NumberRange
from app.models import Ticket


class EditTicketForm(FlaskForm):
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
