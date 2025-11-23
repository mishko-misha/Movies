from flask import render_template, request, redirect, url_for, flash, session, get_flashed_messages
from . import auth_bp

@auth_bp.route('/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        lastname = request.form.get('lastname', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        errors = {}

        if not username:
            errors['username'] = 'Username is required.'
        if not lastname:
            errors['lastname'] = 'Last name is required.'
        if not email or '@' not in email:
            errors['email'] = 'A valid email is required.'
        if not password or len(password) < 6:
            errors['password'] = 'Password must be at least 6 characters long.'

        if errors:
            flash(errors, 'error')
            session['form_data'] = {'username': username, 'lastname': lastname, 'email': email}
            return redirect(url_for('auth.user_register'))

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.user_login'))

    flashed = get_flashed_messages(with_categories=True)
    errors = next((msg for cat, msg in flashed if cat == 'error'), None)
    success = next((msg for cat, msg in flashed if cat == 'success'), None)
    form_data = session.pop('form_data', {})

    return render_template(
        'register.html',
        errors=errors,
        username=form_data.get('username', ''),
        lastname=form_data.get('lastname', ''),
        email=form_data.get('email', ''),
        success=success
    )

@auth_bp.route('/login', methods=['GET','POST'])
def user_login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        errors = {}

        if not username:
            errors['username'] = 'Username is required.'
        if not password:
            errors['password'] = 'Password is required.'

        if errors:
            flash(errors, 'error')
            session['form_data'] = {'username': username, 'password': password}
            return redirect(url_for('auth.user_login'))

        flash('Login successful!', 'success')
        return redirect(url_for('main_page'))

    flashed = get_flashed_messages(with_categories=True)
    errors = next((msg for cat, msg in flashed if cat == 'error'), None)
    success = next((msg for cat, msg in flashed if cat == 'success'), None)
    form_data = session.pop('form_data', {})

    return render_template(
        'login.html',
        errors=errors,
        username=form_data.get('username', ''),
        password=form_data.get('password', ''),
        success=success
    )