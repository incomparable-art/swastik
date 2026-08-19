from datetime import datetime
from flask import render_template, request, jsonify, url_for, redirect
from swastikapp.database.db import MongoDatabase
from flask_login import current_user


def customer():
    templateData = {'page': "customer"}
    return render_template("admin/customer/customer.html", **templateData)

def add_customer():
    name = request.form.get('c_name')
    address = request.form.get('c_address')
    tin = request.form.get('c_tin')
    contact = request.form.get('c_contact')

    with MongoDatabase() as mongo:

        # 1. Check if user already exists
        if mongo.get_customer_by_tin(tin):
            return jsonify({'status': 'error',
                            'message': f'An Customer with this {tin} already exists'
                            }), 400

        # 2. Create user and get User object back
        now_str = datetime.now().strftime("%a %b %d %H:%M:%S %Y")
        customer_doc = {
            "name": name,
            "address": address,
            "tin": tin,
            "contact": contact,
            "user": current_user.email,
            "is_active": True,
            "created_date": now_str,
            "updated_date": now_str
        }
        res = mongo.db.customer.insert_one(customer_doc)
        return jsonify({'status': 'success',
                        'message': f'{name} with {tin} stored in Database'
                        }), 200

def get_customer(customer_id):
    # Fetch user from database
    with MongoDatabase() as mongo:
        # 2. Check if user already exists
        customer =  mongo.get_customer_by_id(id=customer_id)

        # Return full dictionary
        return jsonify({
            'id': customer_id,
            'name': customer.name,
            'address': customer.address,
            'tin': customer.tin,
            'contact': customer.contact
        }), 200

def get_customers():
    with MongoDatabase() as mongo:
        # Fetch all users as User objects
        customers = mongo.get_all_customers()
        # Convert each Customer instance to a dictionary
        customers_list = [customer.to_dict() for customer in customers]
        return jsonify({
            'customers': customers_list  # Wrapped inside a dictionary
        }), 200

def delete_customer(customer_id):
    # Fetch user from database
    with MongoDatabase() as mongo:
        # 1. Check if customer exists
        customer = mongo.get_customer_by_id(id=customer_id)
        if not customer:
            return jsonify({"status": "error", "message": "Customer not found"}), 404

        # 2. Perform deletion
        success = mongo.delete_customer_by_id(id=customer_id)

        if success:
            return jsonify({
                "status": "success",
                "message": "Customer deleted successfully!"
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Failed to delete customer from database."
            }), 500

def update_customer():
    customer_id = request.form.get('editCustomerId')
    name = request.form.get('editName')
    address = request.form.get('editAddress')
    tin = request.form.get('editTin')
    contact = request.form.get('editContact')

    now_str = datetime.now().strftime("%a %b %d %H:%M:%S %Y")

    with MongoDatabase() as mongo:
        update_data = {
            "name": name,
            "address": address,
            "tin": tin,
            "contact": contact,
            "user" :current_user.email,
            "updated_date": now_str
        }

        success = mongo.update_customer(id=customer_id, data=update_data)

        if success:
            return jsonify({
                "status": "success",
                "message": "Customer updated successfully!"
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Failed to update customer"
            }), 500
