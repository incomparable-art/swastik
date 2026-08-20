from swastikapp import login_manager, bcrypt
from flask import render_template, request, flash, redirect, session, url_for
from flask_login import login_user, logout_user, current_user
from swastikapp.database.db import User, MongoDatabase

# ✅ Put @login_manager.user_loader HERE inside main file
@login_manager.user_loader
def load_user(user_id):
    with MongoDatabase() as mongo:
        return mongo.get_user_by_id(user_id)

def signup():
    # Redirect if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('route_dashboard'))

    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            contact = request.form.get('phone')
            password = request.form.get('password')

            pw_hash = bcrypt.generate_password_hash(password)

            with MongoDatabase() as mongo:
                # 2. Check if user already exists
                if mongo.get_user_by_email(email):
                    flash("An account with this email already exists.", "warning")
                    return redirect(url_for('route_signup'))

                # 3. Create user and get User object back
                new_user = mongo.create_user(
                    name=name,
                    email=email,
                    password_hash=pw_hash,
                    contact=contact,
                    role="user"
                )
                print(new_user)

                flash("Your account successfully created.", "info")
                return redirect(url_for('route_admin_login'))
        except Exception as exp:
            print('add_user() :: Got exception: %s' % exp)
            return redirect(url_for('route_signup'))
    else:
        return render_template("admin/signup.html")

def login():
    # Redirect if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('route_dashboard'))

    if request.method == 'POST':
        try:
            email = request.form.get('email')
            password = request.form.get('password')
            remember = True if request.form.get('remember') else False

            with MongoDatabase() as mongo:
                user = mongo.get_user_by_email(email)
                # Check password hash (handling bytes or str)
                if user and bcrypt.check_password_hash(user.pw_hash, password):
                    if user.role == "admin" or user.role == "super_admin":
                        # Wrap in User class and log in directly
                        session.permanent = True
                        login_user(user, remember=remember)
                        return redirect(url_for('route_dashboard'))
                    else:
                        flash("You can't access this without admin permission. ", "danger")
                        return redirect(url_for('route_admin_login'))
                else:
                    flash("Invalid email or password.", "danger")
                    return redirect (url_for('route_admin_login'))

        except Exception as e:
            print(e)
            return redirect(url_for('route_admin_login'))
    else:
        return render_template('admin/login.html')

def logout():
    # Clears user session from Flask-Login
    logout_user()
    session.permanent = False

    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('route_admin_login'))
