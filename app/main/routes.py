from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.models import User
from app.main import bp
from app.main.forms import EditProfileForm
import sqlalchemy as sa


@bp.route('/')
def index():
    return render_template('index.html', title='Početna')


@bp.route('/profile/<username>')
@login_required
def profile(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    return render_template('profile.html', title='Moj profil', user=user)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.balance = form.balance.data
        db.session.commit()
        flash('Promjene su spremljene.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.balance.data = current_user.balance

    return render_template('edit_profile.html', title='Uredi Profil', form=form)
