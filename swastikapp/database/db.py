import os, re
import math
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from swastikapp.database.user import User
from swastikapp.database.customer import Customer
from swastikapp.database.invoice import Invoice

load_dotenv()

# Database Setup
db_name = os.getenv("DATABASE_NAME")
connection_string = os.getenv("CONNECTION_STRING")

from bson import ObjectId

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

    #################################################################################
    #                                                                               #
    #                 HELPER QUERIES RETURNING INVOICE OBJECTS                      #
    #                                                                               #
    #################################################################################
    def get_paginated_invoices(self, page=1, per_page=10, filter_query=None,
                               sort_field="_id"):
        """
        Fetches paginated records along with pagination metadata.
        """
        if filter_query is None:
            filter_query = {}

        total_records = self.db.invoices.count_documents(filter_query)
        total_pages = math.ceil(total_records / per_page) if total_records > 0 else 1

        # 2. Skip calculation: (page - 1) * per_page
        skip_count = (page - 1) * per_page

        # 3. Query with skip and limit
        cursor = (
            self.db.invoices.find(filter_query)
            .sort(sort_field, pymongo.DESCENDING)
            .skip(skip_count)
            .limit(per_page)
        )

        invoices = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            invoices.append(doc)
        print(invoices)

        return {
            "invoices": invoices,
            "page": page,
            "per_page": per_page,
            "total_records": total_records,
            "total_pages": total_pages,
            "has_prev": page > 1,
            "has_next": page < total_pages,
            "prev_num": page - 1,
            "next_num": page + 1
        }

    def get_all_invoices(self, limit: int = 10) -> list[Invoice]:
        """Retrieves all users from MongoDB and returns a list of User objects."""
        # find({}) retrieves all documents
        invoice_cursor = self.db.invoices.find({})

        if limit > 0:
            invoice_cursor = invoice_cursor.limit(limit)

        return [Invoice(doc) for doc in invoice_cursor]

    def get_invoice_by_id(self, invoice_id: str) -> Invoice | None:
        """Finds a user document by string ObjectId and returns a User object."""
        try:
            invoice_doc = self.db.invoices.find_one({"_id": ObjectId(invoice_id)})
            return Invoice(invoice_doc) if invoice_doc else None
        except Exception:
            return None

    def get_invoices_by_status(self, status: str) -> list[Invoice]:
        """Fetch all invoices based on status'."""
        try:
            # Query documents based on status
            cursor = self.db.invoices.find({"status": status}).sort("_id", -1)

            status_list = []
            for doc in cursor:
                doc["_id"] = str(doc["_id"])  # ObjectId to string conversion
                status_list.append(doc)

            return status_list
        except Exception as e:
            print(f"Error fetching deleted invoices: {e}")
            return []

    def get_next_invoice_number_from_last(self):
        """
        Fetches the latest invoice and increments its numerical value by 1.
        """
        # Sabse latest invoice fetch karein (created_date ya _id ke basis par descending sort)
        last_invoice = self.db.invoices.find_one(sort=[("_id", -1)])

        if not last_invoice or "invoice_no" not in last_invoice:
            return "INV-0001"  # Default starting invoice number

        last_invoice_no = str(last_invoice["invoice_no"])

        # Numbers extract karein (e.g., 'INV-0042' se 42 nikalna)
        digits = re.findall(r'\d+', last_invoice_no)
        if digits:
            next_num = int(digits[-1]) + 1
            return f"INV-{next_num:04d}"
        else:
            return "INV-0001"

    def update_invoice(self, id, data):
        """Update fields for a specific invoice."""
        try:
            query_id = ObjectId(id) if isinstance(id, str) and ObjectId.is_valid(id) else id
            result = self.db.invoices.update_one(
                {"_id": query_id},
                {"$set": data}
            )
            return result.matched_count > 0
        except Exception as e:
            print(f"Error updating invoice: {e}")
            return False

    def update_invoice_status(self, invoice_id: str, new_status: str) -> bool:
        """Updates only the status field of an invoice by its ID."""
        try:
            result = self.db.invoices.update_one(
                {"_id": ObjectId(invoice_id)},  # Filter by ID
                {"$set": {"status": new_status}}  # Only updates the status field
            )
            return result.modified_count > 0 or result.matched_count > 0
        except Exception as e:
            print(f"Error updating status: {e}")
            return False

    #################################################################################
    #                                                                               #
    #                     HELPER QUERIES RETURNING USER OBJECTS                     #
    #                                                                               #
    #################################################################################
    def create_user(self, name: str, email: str, password_hash: bytes | str, contact: str = "",
                    role: str = "user", is_active: bool = True) -> User:
        now_str = datetime.now().strftime("%a %b %d %H:%M:%S %Y")

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
        now_str = datetime.now().strftime("%a %b %d %H:%M:%S %Y")

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