from flask import render_template, flash, redirect, url_for, abort, request
from flask_login import current_user, login_required
from flask_paginate import Pagination, get_page_args
from app import db
from app.admin import bp
from app.admin.forms import EditTicketForm
from app.models import Ticket, Order, User


@bp.route('/')
@bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin:
        return redirect(url_for('auth.login'))
    else:
        total_users = User.query.count()
        total_tickets = Ticket.query.count()
        total_orders = Order.query.count()

        return render_template('admin/dashboard.html', title='Administracija', total_users=total_users, total_tickets=total_tickets, total_orders=total_orders)


@bp.route('/users')
@login_required
def view_users():
    if not current_user.is_admin:
        return redirect(url_for('auth.login'))
    pass


@bp.route('/tickets')
@login_required
def view_tickets():
    if not current_user.is_admin:
        return redirect(url_for('auth.login'))
    per_page = request.args.get('per_page', 5, type=int)
    pagination = Ticket.query.order_by(Ticket.id).paginate(per_page=per_page)
    return render_template('admin/tickets.html', pagination=pagination)


@bp.route('/add_ticket')
@login_required
def add_ticket():
    if not current_user.is_admin:
        return redirect(url_for('auth.login'))
    else:
        pass


@bp.route('/admin/edit_ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def edit_ticket(ticket_id):
    if not current_user.is_admin:
        return redirect(url_for('login'))

    ticket = Ticket.query.get_or_404(ticket_id)

    form = EditTicketForm(obj=ticket)

    if form.validate_on_submit():
        form.populate_obj(ticket)
        db.session.commit()
        flash('Karta uspješno ažurirana.', 'success')
        return redirect(url_for('admin.edit_ticket', ticket_id=ticket_id))

    return render_template('admin/edit_ticket.html', form=form, ticket=ticket)


@bp.route('/delete_ticket/<ticket_id>')
@login_required
def delete_ticket(ticket_id):
    if not current_user.is_admin:
        return redirect(url_for('auth.login'))
    else:
        pass


@bp.route('/orders')
@login_required
def view_orders():
    if not current_user.is_admin:
        return redirect(url_for('auth.login'))
    pass
