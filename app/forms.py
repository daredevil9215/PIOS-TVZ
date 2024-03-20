from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField, FloatField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length, NumberRange
import sqlalchemy as sa
from app import db
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Korisničko Ime', validators=[
                           DataRequired("Korisničko ime je obavezno.")])
    password = PasswordField('Lozinka', validators=[
                             DataRequired("Lozinka je obavezna.")])
    remember_me = BooleanField('Zapamti Prijavu')
    submit = SubmitField('Prijavi Se')


class RegistrationForm(FlaskForm):
    username = StringField('Korisničko Ime', validators=[
                           DataRequired(message="Korisničko ime je obavezno.")])
    password = PasswordField('Lozinka', validators=[
                             DataRequired("Lozinka je obavezna.")])
    password2 = PasswordField(
        'Ponovi Lozinku', validators=[DataRequired("Lozinka je obavezna."), EqualTo('password')]
    )
    submit = SubmitField('Registriraj Se')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data
        ))
        if user is not None:
            raise ValidationError('Molimo koristite drugo korisničko ime')


class EditProfileForm(FlaskForm):
    username = StringField('Korisničko ime', validators=[
                           DataRequired(message="Korisničko ime je obavezno.")])
    balance = FloatField('Stanje računa', validators=[DataRequired(message="Stanje računa je obavezno."
                                                                   ), NumberRange(min=0, max=float('inf'), message='Stanje računa ne smije biti negativno.')])
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
