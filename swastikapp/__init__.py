import os
from flask_mail import Mail, Message
from flask import Flask, render_template, request, flash, redirect, session, url_for, g
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import timedelta
from email.utils import formataddr
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import traceback
from swastikapp.database import User

app = Flask(__name__)

app.config['secretkey'] = os.getenv("SECRET_KEY")
app.secret_key = os.getenv("SECRET_KEY")

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
login_manager.login_view = "route_admin_login"  # Redirects unauthenticated users here
login_manager.login_message_category = "info"

app.permanent_session_lifetime = timedelta(minutes=30)

from swastikapp import routes