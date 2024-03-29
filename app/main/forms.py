from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, PasswordField
from wtforms.validators import ValidationError, DataRequired, EqualTo, NumberRange
import sqlalchemy as sa
from app import db
from app.models import User


class EditProfileForm(FlaskForm):
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
    balance = FloatField('Stanje računa',
                         validators=[DataRequired(message="Stanje računa je obavezno."),
                                     NumberRange(min=0, max=float('inf'), message='Stanje računa ne smije biti negativno.')])
    balance = FloatField('Stanje računa',
                         validators=[DataRequired(message="Stanje računa je obavezno."),
                                     NumberRange(min=0, max=float('inf'), message='Stanje računa ne smije biti negativno.')])
    submit = SubmitField('Spremi')

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(
                User.username == self.username.data))
            if user is not None:
                raise ValidationError('Molimo koristite drugo korisničko ime.')
