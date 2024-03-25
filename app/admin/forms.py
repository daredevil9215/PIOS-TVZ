from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import ValidationError, DataRequired, EqualTo, NumberRange
from app.models import Ticket


class EditTicketForm(FlaskForm):
    name = StringField('Ime', validators=[
        DataRequired(message="Ime je obavezno.")])
    price = FloatField('Cijena', validators=[
        DataRequired(message="Cijena je obavezna.")
    ])
    route = StringField('Linija',
                        validators=[])
    submit = SubmitField('Spremi Promjene')
