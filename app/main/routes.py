from flask import render_template, flash, redirect, url_for, request, jsonify, session
from flask_login import current_user, login_required
from app import db
from app.models import User, Ticket, Order, OrderTicket
from app.main import bp
from app.main.forms import EditProfileForm
import sqlalchemy as sa


@bp.route('/')
def index():
    tickets = Ticket.query.all()
    return render_template('index.html', title='Početna', tickets=tickets)


@bp.route('/search', methods=['POST'])
def search_tickets():
    search_query = request.form['search_query']
    # Query the database for tickets matching the search query
    # Here, 'name' is assumed to be a column in the Ticket model
    tickets = Ticket.query.filter(
        Ticket.name.ilike(f"%{search_query}%")).all()
    return render_template('search_results.html', tickets=tickets, search_query=search_query)


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


@bp.route('/cart', methods=['GET'])
def view_cart():
    cart = session.get('cart', {})
    total_amount = sum(item['price'] * item['quantity']
                       for item in cart.values())
    return render_template('cart.html', cart=cart, total_amount=total_amount)


@bp.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    ticket_id = request.form.get('ticket_id')
    # default 1 if not provided
    quantity = int(request.form.get('quantity', 1))
    if not ticket_id:
        flash('Krivi identifikacijski broj karte.', 'error')
        return jsonify({'success': False})

    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        flash('Karta nije pronađena.', 'error')
        return jsonify({'success': False})

    cart = session.get('cart', {})
    cart[ticket_id] = {'name': ticket.name,
                       'price': ticket.price, 'quantity': quantity}
    session['cart'] = cart

    flash('Karta dodana u košaricu.', 'success')
    return jsonify({'success': True, 'redirect_url': url_for('main.index')})


@bp.route('/update_cart/<item_id>', methods=['POST'])
def update_cart(item_id):
    new_quantity = int(request.form['quantity'])
    cart_items = session.get('cart', {})
    if item_id in cart_items:
        cart_items[item_id]['quantity'] = new_quantity
        session['cart'] = cart_items
        flash('Košarica je ažurirana.', 'success')
        return redirect(url_for('main.view_cart'))
    else:
        flash('Karta nije pronađena.', 'error')
        return redirect(url_for('main.view_cart'))


@bp.route('/remove_from_cart/<item_id>', methods=['POST'])
def remove_from_cart(item_id):
    cart = session.get('cart', [])
    for item_id in cart:
        del cart[item_id]
        break
    session['cart'] = cart
    flash('Karta izbrisana iz košarice', 'success')
    return redirect(url_for('main.view_cart'))


@bp.route('/checkout', methods=['GET'])
@login_required
def checkout():
    cart = session.get('cart', {})
    total_amount = sum(item['price'] * item['quantity']
                       for item in cart.values())
    if total_amount == 0:
        flash('Nemate karte u košarici.', 'error')
        return redirect(url_for('main.index'))
    user_balance = current_user.balance
    return render_template('checkout.html', user_balance=user_balance, total_amount=total_amount, cart=cart)


@bp.route('/process_payment', methods=['POST'])
@login_required
def process_payment():
    user_balance = current_user.balance
    cart = session.get('cart', {})
    total_amount = sum(item['price'] for item in cart.values())
    payment_method = request.form.get('payment_method')
    if total_amount <= user_balance:
        user_balance -= total_amount
        order = Order(user_id=current_user.id,
                      total_amount=total_amount, payment_method=payment_method)
        db.session.add(order)
        db.session.commit()
        order_id = order.id
        for item_id, item_info in cart.items():
            order_ticket = OrderTicket(
                order_id=order_id, ticket_id=item_id, quantity=item_info.get('quantity', 0))
            db.session.add(order_ticket)
        db.session.commit()
        session.pop('cart', None)
        flash('Plaćanje uspješno!', 'success')
    else:
        flash('Nemate dovoljno sredstava na računu.', 'error')
    return redirect(url_for('main.index'))
