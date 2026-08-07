import os
# import certifi
from pymongo import MongoClient
from flask_login import UserMixin
from bson import ObjectId
from dotenv import load_dotenv
import datetime

load_dotenv()

# Database Setup
database_name = os.getenv("DATABASE_NAME")
client = MongoClient(os.getenv("CONNECTION_STRING"))
db = client[database_name]

# User wrapper class for Flask-Login
class User(UserMixin):
    def __init__(self, user_doc):
        self.id = str(user_doc['_id'])
        self.name = user_doc.get('name', '')
        self.email = user_doc.get('email', '')
        self.contact = user_doc.get('contact', '')
        self.pw_hash = user_doc.get('password', '')
        self.role = user_doc.get('role', 'user')
        self.created_date = user_doc.get('created_date', '')
        self.updated_date = user_doc.get('updated_date', '')

    def check_password(self, password, bcrypt):
        return bcrypt.check_password_hash(self.pw_hash, password)

    @property
    def is_admin(self):
        print(self.role, "role")
        return self.role == 'admin'

    @staticmethod
    def get_by_id(user_id):
        try:
            user_doc = db.user.find_one({'_id': ObjectId(user_id)})
            return User(user_doc) if user_doc else None
        except Exception:
            return None

    # Static loader method by Email
    @staticmethod
    def get_by_email(email):
        user_doc = db.user.find_one({'email': email})
        return User(user_doc) if user_doc else None

    @staticmethod
    def insert_id(user_id):
        try:
            user_doc = db.user.find_one({'_id': ObjectId(user_id)})
            return User(user_doc) if user_doc else None
        except Exception:
            return None

    @staticmethod
    def add_user(name, email, contact, pw_hash):
        try:
            timestamp1 = datetime.datetime.today().strftime("%a %b %d %X %Y")
            timestamp2 = datetime.datetime.today().strftime("%a %b %d %X %Y")
            rec = {
                'name': name,
                'email': email,
                'contact': contact,
                'password': pw_hash,
                'role': 'user',
                'created_date': timestamp1,
                'updated_date': timestamp2
            }
            return db.user.insert_one(rec)
        except Exception:
            return None
