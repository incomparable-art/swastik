from swastikapp import *
# from flask import render_template, request, flash, redirect, session, url_for
# from flask_login import login_user, logout_user, current_user
# from swastikapp.database import User


# ✅ Put @login_manager.user_loader HERE inside main file
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


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

            existing_user = User.get_by_email(email)
            if existing_user:
                flash("An account with this email already exists.", "warning")
                return redirect(url_for('route_signup'))

            pw_hash = bcrypt.generate_password_hash(password)

            User.add_user(name, email, contact, pw_hash)
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

            # Look up user in MongoDB
            user = User.get_by_email(email)

            if user.role == "admin":
                # Verify existence and password hash
                if user and bcrypt.check_password_hash(user.pw_hash, password):
                    # Wrap in User class and log in directly
                    session.permanent = True
                    login_user(user, remember=remember)

                    # Redirect to originally requested page if 'next' param exists
                    next_page = request.args.get('next')
                    return redirect(next_page or url_for('route_dashboard'))
                else:
                    flash("Invalid email or password.", "danger")
                    return redirect (url_for('route_admin_login'))
            else:
                flash("You can't access this without admin permission. ", "danger")
                return redirect(url_for('route_admin_login'))
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
