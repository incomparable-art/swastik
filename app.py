from flask import Flask, render_template, request, flash, redirect, session, url_for, g
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import timedelta
from flask_mail import Mail, Message
from email.utils import formataddr
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
import traceback
from db import User

app = Flask(__name__)

load_dotenv()

app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = os.getenv("MAIL_PORT")
app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS")
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

# Initialize Extensions
bcrypt = Bcrypt(app)
mail = Mail(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"  # Redirects unauthenticated users here
login_manager.login_message_category = "info"

SESSION_TIME = int(os.getenv("SESSION_TIME"))
# 1. Configure session lifetime at app setup (NOT inside a request hook)
app.permanent_session_lifetime = timedelta(minutes=SESSION_TIME)

# 2. Use a before_request hook for request-level logic
@app.before_request
def before_request():
    # Make the current session permanent (uses the 30 min lifetime set above)
    session.permanent = True
    session.modified = True
    # Assign current_user to flask.g if your app relies on g.user
    g.user = current_user


# ✅ Put @login_manager.user_loader HERE inside app.py
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        company = request.form.get('company')
        phone = request.form.get('phone')
        email = request.form.get('email')
        model = request.form.get('model')
        service = request.form.get('service')
        detail = request.form.get('detail')

        try:
            html = render_template(
                "emails/service_request.html",
                name = name,
                company = company,
                phone = phone,
                email = email,
                model = model,
                service = service,
                detail = detail
            )
            service_team = os.getenv("SERVICE_TEAM")
            sales_team = os.getenv("SALES_TEAM")

            msg = Message(
                subject="🔧 New Service Request | Swastik Technology & Services",
                sender=formataddr(("Swastik Technology & Services", "247668.swastik@gmail.com")),
                recipients=[
                    formataddr(("Service Team", service_team))
                ],
                cc=[
                    formataddr(("Customer", email)),
                    formataddr(("Sales Team", sales_team))
                ]
            )

            msg.html = html
            mail.send(msg)
            flash('Email Sent Successfully!')
            return redirect(url_for('dashboard'))
        except Exception as e:
            print(e)
            return render_template('index.html')
    else:
        return render_template('index.html')


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template("admin/dashboard.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

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
                    return redirect(next_page or url_for('dashboard'))
                else:
                    flash("Invalid email or password.", "danger")
                    return redirect (url_for('login'))
            else:
                flash("You can't access this without admin permission. ", "danger")
                return redirect(url_for('login'))
        except Exception as e:
            print(e)
            return redirect(url_for('login'))
    else:
        return render_template('admin/sign-in.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Redirect if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            contact = request.form.get('phone')
            password = request.form.get('password')

            existing_user = User.get_by_email(email)
            if existing_user:
                flash("An account with this email already exists.", "warning")
                return redirect(url_for('signup'))

            pw_hash = bcrypt.generate_password_hash(password)

            User.add_user(name, email, contact, pw_hash)
            flash("Your account successfully created.", "info")

            return redirect(url_for('login'))

        except Exception as exp:
            print('add_user() :: Got exception: %s' % exp)
            return redirect(url_for('signup'))
    else:
        return render_template("admin/sign-up.html")


@app.route('/logout')
@login_required
def logout():
    # Clears user session from Flask-Login
    logout_user()
    session.permanent = False

    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG"))
