from flask import render_template, flash, redirect, url_for, request, jsonify, session, send_from_directory
from flask_login import current_user, login_required
from app import db
from app.models import User, Ticket, Order, OrderTicket
from app.main import bp
from app.main.forms import EditProfileForm, ChangePasswordForm
import sqlalchemy as sa


def index():
    """
    Render the index page.

    This function renders the index page of the application.

    :return: HTML content of the index page.
    """
    tickets = Ticket.query.all()
    return render_template('index.html', title='Početna', tickets=tickets)

def search_tickets():
    """
    Render the search page.

    This function renders the search page of the application.

    :return: HTML content of the search page.
    """
    search_query = request.form['search_query']
    # Query the database for tickets matching the search query
    # Here, 'name' is assumed to be a column in the Ticket model
    tickets = Ticket.query.filter(
        Ticket.name.ilike(f"%{search_query}%")).all()
    return render_template('search_results.html', tickets=tickets, search_query=search_query)

def profile(username):
    """
    Render the profile page.

    This function renders the profile page of the application.

    :return: HTML content of the profile page.
    """
    user = db.first_or_404(sa.select(User).where(User.username == username))
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', title='Moj profil', user=user, orders=orders)

def edit_profile():
    """
    Render the edit profile page.

    This function renders the edit profile page of the application.

    :return: HTML content of the edit profile page.
    """
    form = EditProfileForm(
        obj=current_user, original_username=current_user.username)
    if form.validate_on_submit():
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.email = form.email.data
        current_user.username = form.username.data
        current_user.balance = form.balance.data
        db.session.commit()
        flash('Profil je ažuriran.', 'success')
        return redirect(url_for('main.profile', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.balance.data = current_user.balance

    return render_template('edit_profile.html', title='Uredi Profil', form=form)

def change_password():
    """
    Change user password.

    This function changes the user password using POST request.

    :return: HTML content of the change password page.
    """
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(
            User.username == current_user.username).first()
        user.set_password(form.password.data)
        db.session.commit()
        flash('Lozinka je promjenjena.', 'success')
        return redirect(url_for('main.profile', username=current_user.username))
    return render_template('change_password.html', title='Promjeni Lozinku', form=form)

def view_cart():
    """
    Render the cart page.

    This function renders the cart page of the application.

    :return: HTML content of the cart page.
    """
    cart = session.get('cart', {})
    total_amount = sum(item['price'] * item['quantity']
                       for item in cart.values())
    return render_template('cart.html', cart=cart, total_amount=total_amount)

def add_to_cart():
    """
    Add an item to cart.

    This function adds an item to cart using POST request.

    :return: JSON response
    """
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

    available_tickets = ticket.total_seats - ticket.reserved_seats

    if quantity > available_tickets:
        flash('Nema dovoljno karata.', 'error')
        return jsonify({'success': True, 'redirect_url': url_for('main.index')})

    ticket.reserved_seats = ticket.reserved_seats + quantity
    db.session.commit()

    cart = session.get('cart', {})
    if ticket_id in cart.keys():
        if cart[ticket_id]['quantity']:
            quantity = quantity + cart[ticket_id]['quantity']
    cart[ticket_id] = {'name': ticket.name,
                       'price': ticket.price, 'quantity': quantity}
    session['cart'] = cart

    flash('Karta dodana u košaricu.', 'success')
    return jsonify({'success': True, 'redirect_url': url_for('main.index')})

def update_cart(item_id):
    """
    Update an item from the cart

    This function updates an item  using POST request.

    :return: HTML content of the cart page.
    """
    ticket = Ticket.query.get(item_id)
    available_tickets = ticket.total_seats - ticket.reserved_seats
    new_quantity = int(request.form['quantity'])
    cart_items = session.get('cart', {})
    if item_id in cart_items:
        if new_quantity > available_tickets:
            flash('Nema dovoljno karata.', 'error')
            return redirect(url_for('main.view_cart'))
        cart_items[item_id]['quantity'] = new_quantity
        session['cart'] = cart_items
        ticket.reserved_seats = ticket.reserved_seats + new_quantity
        db.session.commit()
        flash('Košarica je ažurirana.', 'success')
        return redirect(url_for('main.view_cart'))
    else:
        flash('Karta nije pronađena.', 'error')
        return redirect(url_for('main.view_cart'))

def remove_from_cart(id):
    """
    Removes an item from the cart

    This function removes an item from the cart using POST request.

    :return: HTML content of the cart page.
    """
    cart = session.get('cart', [])
    for item_id in cart:
        if item_id == id:
            ticket = Ticket.query.get(item_id)
            ticket.reserved_seats = ticket.reserved_seats - \
                cart[item_id]['quantity']
            db.session.commit()
            del cart[item_id]
            break
    session['cart'] = cart
    flash('Karta izbrisana iz košarice', 'success')
    return redirect(url_for('main.view_cart'))

def checkout():
    cart = session.get('cart', {})
    total_amount = sum(item['price'] * item['quantity']
                       for item in cart.values())
    if total_amount == 0:
        flash('Nemate karte u košarici.', 'error')
        return redirect(url_for('main.index'))
    user_balance = current_user.balance
    return render_template('checkout.html', user_balance=user_balance, total_amount=total_amount, cart=cart)

def process_payment():
    user_balance = current_user.balance
    cart = session.get('cart', {})
    total_amount = sum(item['price'] * item['quantity']
                       for item in cart.values())
    payment_method = request.form.get('payment_method')
    if total_amount <= user_balance:
        user_balance = user_balance - total_amount
        db.session.query(User).filter(
            User.username == current_user.username).update({"balance": user_balance})
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
        from app.email import send_order_successful_email
        user = db.session.query(User).filter(
            User.username == current_user.username).first()
        send_order_successful_email(user, order)
        flash('Plaćanje uspješno!', 'success')
    else:
        flash('Nemate dovoljno sredstava na računu.', 'error')
    return redirect(url_for('main.index'))

def serve_docs(path):
    return send_from_directory('docs/_build/html', path)
