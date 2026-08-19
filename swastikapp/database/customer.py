from flask_login import UserMixin
from datetime import datetime

# -------------------------------------------------------------
# 1. Flask-Login Customer Model (Data Object Wrapper)
# -------------------------------------------------------------
class Customer(UserMixin):
    def __init__(self, customer_doc: dict):
        # Flask-Login requires self.id to be a string
        self.id = str(customer_doc['_id'])
        self.name = customer_doc.get('name', '')
        self.address = customer_doc.get('address', '')
        self.tin = customer_doc.get('tin', '')
        self.contact = customer_doc.get('contact', '')
        self.user = customer_doc.get('email', '')

        self.created_date = customer_doc.get('created_date', '')
        self.updated_date = customer_doc.get('updated_date', '')

    def to_dict(self):
        """Converts the Customer instance attributes into a JSON-serializable dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'tin': self.tin,
            'contact': self.contact,
            'user': self.user,
            'created_date': self.created_date.isoformat() if isinstance(self.created_date, datetime) else str(self.created_date),
            'updated_date': self.updated_date.isoformat() if isinstance(self.updated_date, datetime) else str(self.updated_date)
        }
