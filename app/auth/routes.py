from flask import render_template, flash, redirect, url_for, abort, request
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, \
    ResetPasswordRequestForm, ResetPasswordForm
from app.models import User
import sqlalchemy as sa


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash('Pogrešan username ili password')
            return redirect(url_for('auth.login'))
        flash('Korisnik {} prijavljen, zapamti={}'.format(
            form.username.data, form.remember_me.data))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('login.html', title='Prijava', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(firstname=form.firstname.data, lastname=form.lastname.data, username=form.username.data, is_admin=False, balance=0)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Čestitamo, sada ste registrirani korisnik!')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Registracija', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
