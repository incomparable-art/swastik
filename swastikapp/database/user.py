from flask_login import UserMixin

# -------------------------------------------------------------
# 1. Flask-Login User Model (Data Object Wrapper)
# -------------------------------------------------------------
class User(UserMixin):
    def __init__(self, user_doc: dict):
        # Flask-Login requires self.id to be a string
        self.id = str(user_doc['_id'])
        self.name = user_doc.get('name', '')
        self.email = user_doc.get('email', '')
        self.contact = user_doc.get('contact', '')
        self.pw_hash = user_doc.get('password', '')
        self.role = user_doc.get('role', 'user')

        self.created_date = user_doc.get('created_date', '')
        self.updated_date = user_doc.get('updated_date', '')

