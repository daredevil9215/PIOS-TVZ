from flask import render_template, flash, redirect, url_for, abort, request, jsonify
from flask_login import current_user, login_required
from flask_paginate import Pagination, get_page_args
from app import db
from app.admin import bp
from app.admin.forms import TicketForm, UserForm, EditOrderForm
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
    per_page = request.args.get('per_page', 5, type=int)
    pagination = User.query.order_by(User.id).paginate(per_page=per_page)
    return render_template('admin/users.html', pagination=pagination)


@bp.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if not current_user.is_admin:
        return redirect(url_for('auth.login'))

    form = UserForm()

    if form.validate_on_submit():
        is_admin = request.form.get('is_admin') == 'True'
        user = User(firstname=form.firstname.data, lastname=form.lastname.data,
                    email=form.email.data, username=form.username.data, balance=form.balance.data, is_admin=is_admin)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Korisnik uspješno kreiran.', 'success')
        return redirect(url_for('admin.view_users'))

    return render_template('admin/add_user.html', form=form)


@bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not current_user.is_admin:
        return redirect(url_for('login'))

    user = User.query.get_or_404(user_id)

    form = UserForm(obj=user)

    if form.validate_on_submit():
        form.populate_obj(user)
        is_admin = request.form.get('is_admin') == 'True'
        user.is_admin = is_admin
        user.set_password(form.password.data)
        db.session.commit()
        flash('Korisnik uspješno ažuriran.', 'success')
        return redirect(url_for('admin.edit_user', user_id=user_id))

    return render_template('admin/edit_user.html', form=form, user=user)


@bp.route('/delete_user/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        return jsonify({'message': 'Unauthorized'}), 401

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'Korisnik uspješno izbrisan.'}), 200


@bp.route('/tickets')
@login_required
def view_tickets():
    if not current_user.is_admin:
        return redirect(url_for('auth.login'))
    per_page = request.args.get('per_page', 5, type=int)
    pagination = Ticket.query.order_by(Ticket.id).paginate(per_page=per_page)
    return render_template('admin/tickets.html', pagination=pagination)


@bp.route('/add_ticket', methods=['GET', 'POST'])
@login_required
def add_ticket():
    if not current_user.is_admin:
        return redirect(url_for('auth.login'))

    form = TicketForm()

    if form.validate_on_submit():
        ticket = Ticket(name=form.name.data, city=form.city.data, route=form.route.data,
                        total_seats=form.total_seats.data, price=form.price.data)
        db.session.add(ticket)
        db.session.commit()
        flash('Karta uspješno kreirana.', 'success')
        return redirect(url_for('admin.view_tickets'))

    return render_template('admin/add_ticket.html', form=form)


@bp.route('/edit_ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def edit_ticket(ticket_id):
    if not current_user.is_admin:
        return redirect(url_for('login'))

    ticket = Ticket.query.get_or_404(ticket_id)

    form = TicketForm(obj=ticket)

    if form.validate_on_submit():
        form.populate_obj(ticket)
        db.session.commit()
        flash('Karta uspješno ažurirana.', 'success')
        return redirect(url_for('admin.edit_ticket', ticket_id=ticket_id))

    return render_template('admin/edit_ticket.html', form=form, ticket=ticket)


@bp.route('/delete_ticket/<int:ticket_id>', methods=['DELETE'])
@login_required
def delete_ticket(ticket_id):
    if not current_user.is_admin:
        return jsonify({'message': 'Unauthorized'}), 401

    ticket = Ticket.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()

    return jsonify({'message': 'Karta uspješno izbrisana.'}), 200


@bp.route('/orders')
@login_required
def view_orders():
    if not current_user.is_admin:
        return redirect(url_for('auth.login'))
    per_page = request.args.get('per_page', 5, type=int)
    pagination = Order.query.order_by(Order.id).paginate(per_page=per_page)
    return render_template('admin/orders.html', pagination=pagination)


@bp.route('/edit_order/<int:order_id>', methods=['GET', 'POST'])
@login_required
def edit_order(order_id):
    if not current_user.is_admin:
        return redirect(url_for('login'))

    order = Order.query.get_or_404(order_id)

    form = EditOrderForm(obj=order)

    if form.validate_on_submit():
        form.populate_obj(order)
        db.session.commit()
        flash('Narudžba uspješno ažurirana.', 'success')
        return redirect(url_for('admin.edit_order', order_id=order_id))

    return render_template('admin/edit_order.html', form=form, order=order)


@bp.route('/delete_order/<int:order_id>', methods=['DELETE'])
@login_required
def delete_order(order_id):
    if not current_user.is_admin:
        return jsonify({'message': 'Unauthorized'}), 401

    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()

    return jsonify({'message': 'Narudžba uspješno izbrisana.'}), 200
