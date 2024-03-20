from flask import render_template, flash, redirect, url_for, abort, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User
import sqlalchemy as sa


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Početna')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash('Pogrešan username ili password')
            return redirect(url_for('login'))
        flash('Korisnik {} prijavljen, zapamti={}'.format(
            form.username.data, form.remember_me.data))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Prijava', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, is_admin=False, balance=0)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Čestitamo, sada ste registrirani korisnik!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registracija', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile/<username>')
@login_required
def profile(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    return render_template('profile.html', title='Moj profil', user=user)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.balance = form.balance.data
        db.session.commit()
        flash('Promjene su spremljene.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.balance.data = current_user.balance

    return render_template('edit_profile.html', title='Uredi Profil', form=form)


@app.route('/admin')
@login_required
def admin_index():
    if current_user.is_admin:
        return render_template('admin.html', title='Administracija')
    else:
        abort(403)
