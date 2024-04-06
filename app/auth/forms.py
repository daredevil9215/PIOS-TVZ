from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
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
    firstname = StringField('Ime', validators=[
        DataRequired(message="Ime je obavezno.")])
    lastname = StringField('Prezime', validators=[
                           DataRequired(message="Prezime je obavezno.")])
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


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        ('Repeat Password'), validators=[DataRequired(),
                                         EqualTo('password')])
    submit = SubmitField(('Request Password Reset'))
