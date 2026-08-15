import os
# import certifi
from pymongo import MongoClient
from flask_login import UserMixin
from bson import ObjectId
from dotenv import load_dotenv
import datetime

# from pymongo.synchronous import database

load_dotenv()
# Connection URI format: mongodb://username:password@host:port/database?authSource=admin
uri = "mongodb://admin:123@localhost:27017/my_database?authSource=admin"

# Pass to MongoClient
client = MongoClient(uri)

# Database Setup
db_name = os.getenv("DATABASE_NAME")
connection_string = os.getenv("CONNECTION_STRING")

from bson import ObjectId


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
            'created_date': self.created_date.isoformat() if isinstance(self.created_date, datetime.datetime) else str(self.created_date),
            'updated_date': self.updated_date.isoformat() if isinstance(self.updated_date, datetime.datetime) else str(self.updated_date)
        }


# -------------------------------------------------------------
# 2. MongoDB Context Manager & Database Layer
# -------------------------------------------------------------
class MongoDatabase:
    def __init__(self, uri=connection_string ,db_name=db_name):
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None

    def __enter__(self):
        self.client = MongoClient(self.uri)
        self.db = self.client[self.db_name]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()

    # --- Helper Queries Returning User Objects ---

    def create_user(
            self,
            name: str,
            email: str,
            password_hash: bytes | str,
            contact: str = "",
            role: str = "user",
            is_active: bool = True
    ) -> User:
        """Inserts a new user into MongoDB and returns the created User object."""
        now_str = datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")

        user_doc = {
            "name": name,
            "email": email,
            "contact": contact,
            "password": password_hash,
            "role": role,
            "is_active": is_active,
            "created_date": now_str,
            "updated_date": now_str
        }

        # insert_one mutates 'user_doc' by adding the generated '_id'
        self.db.user.insert_one(user_doc)

        # Return the new User object (now has '_id' populated)
        return User(user_doc)

    def get_user_by_email(self, email: str) -> User | None:
        """Finds a user document by email and returns a User object."""
        user_doc = self.db.user.find_one({"email": email})
        return User(user_doc) if user_doc else None

    def get_customer_by_tin(self, tin: str) -> Customer | None:
        """Finds a user document by tin and returns a Customer object."""
        customer_doc = self.db.customer.find_one({"tin": tin})
        return Customer(customer_doc) if customer_doc else None

    def get_user_by_id(self, user_id: str) -> User | None:
        """Finds a user document by string ObjectId and returns a User object."""
        try:
            user_doc = self.db.user.find_one({"_id": ObjectId(user_id)})
            return User(user_doc) if user_doc else None
        except Exception:
            return None

    def get_all_users(self, limit: int = 10) -> list[User]:
        """Retrieves all users from MongoDB and returns a list of User objects."""
        # find({}) retrieves all documents
        user_cursor = self.db.user.find({})

        if limit > 0:
            user_cursor = user_cursor.limit(limit)

        return [User(doc) for doc in user_cursor]

    ######################################################################################
    #                                   Customer
    #####################################################################################
    def create_customer(
            self,
            name: str,
            address: str,
            tin: bytes | str,
            contact: str = "",
            user: str = "",
            is_active: bool = True
    ) -> Customer:
        """Inserts a new customer into MongoDB and returns the created Customer object."""
        now_str = datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")

        customer_doc = {
            "name": name,
            "address": address,
            "tin": tin,
            "contact": contact,
            "user": user,
            "is_active": is_active,
            "created_date": now_str,
            "updated_date": now_str
        }

        # insert_one mutates 'customer_doc' by adding the generated '_id'
        self.db.customer.insert_one(customer_doc)

        # Return the new Customer object (now has '_id' populated)
        return Customer(customer_doc)

    def to_dict(self):
        return {
            'id': str(self.id),
            'username': self.username,
            'email': self.email,
            'phone': self.phone
        }

    def update_customer(self, id, data):
        """Update fields for a specific customer."""
        try:
            query_id = ObjectId(id) if isinstance(id, str) and ObjectId.is_valid(id) else id
            result = self.db.customer.update_one(
                {"_id": query_id},
                {"$set": data}
            )
            return result.matched_count > 0
        except Exception as e:
            print(f"Error updating customer: {e}")
            return False

    def get_customer_by_tin(self, tin: str) -> Customer | None:
        """Finds a user document by tin and returns a Customer object."""
        customer_doc = self.db.customer.find_one({"tin": tin})
        return Customer(customer_doc) if customer_doc else None

    def get_customer_by_id(self, id: str) -> Customer | None:
        """Finds a user document by tin and returns a Customer object."""
        customer_doc = self.db.customer.find_one({"_id": ObjectId(id)})
        return Customer(customer_doc) if customer_doc else None


    def get_all_customers(self, limit: int = 10) -> list[Customer]:
        """Retrieves all users from MongoDB and returns a list of User objects."""
        # find({}) retrieves all documents
        customer_cursor = self.db.customer.find({})

        if limit > 0:
            customer_cursor = customer_cursor.limit(limit)

        return [Customer(doc) for doc in customer_cursor]

    def delete_customer_by_id(self, id):
        """Delete a single customer document by string ID or ObjectId."""
        try:
            query_id = ObjectId(id) if isinstance(id, str) and ObjectId.is_valid(id) else id
            result = self.db.customer.delete_one({"_id": query_id})

            # Returns True if a document was deleted, False if no match was found
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting customer: {e}")
            return False