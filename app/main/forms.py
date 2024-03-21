from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import ValidationError, DataRequired, EqualTo, NumberRange
import sqlalchemy as sa
from app import db
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField('Korisničko ime', validators=[
                           DataRequired(message="Korisničko ime je obavezno.")])
    balance = FloatField('Stanje računa',
                         validators=[DataRequired(message="Stanje računa je obavezno."),
                                     NumberRange(min=0, max=float('inf'), message='Stanje računa ne smije biti negativno.')])
    submit = SubmitField('Pošalji')

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(
                User.username == self.username.data))
            if user is not None:
                raise ValidationError('Molimo koristite drugo korisničko ime.')
