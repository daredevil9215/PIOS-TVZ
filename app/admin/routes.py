from flask import render_template, flash, redirect, url_for, abort, request
from flask_login import current_user, login_required
from app import db
from app.admin import bp

@bp.route('/admin')
@login_required
def index():
    if current_user.is_admin:
        return render_template('admin.html', title='Administracija')
    else:
        abort(403)
