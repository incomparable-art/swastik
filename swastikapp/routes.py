from swastikapp import app
from swastikapp.views.admin.account import login, signup, logout
from swastikapp.views.admin.dashboad import (
    dashboard, tables, billing, virtual, rtl, profile, customer, add_customer, get_customer,
    get_customers, update_customer, delete_customer, bill)
from swastikapp.views.user.website import index
from flask_login import login_required

#####################################################################
#                           Direct access                           #
#####################################################################
@app.route('/', methods=['GET', 'POST'])
def route_index():
    return index()

@app.route('/signup', methods=['GET', 'POST'])
def route_signup():
    return signup()

@app.route('/login', methods=['GET', 'POST'])
def route_admin_login():
    return login()



#####################################################################
#                            API Access                            #
#####################################################################
@app.route('/api/add-customer', methods=['POST'])
def route_add_customer():
    return add_customer()

@app.route('/api/get-customer/<customer_id>', methods=['GET'])
def route_get_customer(customer_id):
    return get_customer(customer_id)

@app.route('/api/get-customers', methods=['GET'])
def route_get_customers():
    return get_customers()

@app.route('/api/update-customer', methods=['POST'])
def route_update_customer():
    return update_customer()

@app.route('/api/delete-customer/<customer_id>', methods=['DELETE'])
def route_delete_customer(customer_id):
    return delete_customer(customer_id)


#####################################################################
#                           Admin Access                            #
#####################################################################
@app.route('/bill', methods=['GET', 'POST'])
@login_required
def route_bill():
    return bill()


#####################################################################
#                           Admin Access                            #
#####################################################################
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def route_dashboard():
    return dashboard()



@app.route('/logout')
@login_required
def route_admin_logout():
    return logout()

@app.route('/tables', methods=['GET', 'POST'])
@login_required
def route_tables():
    return tables()

@app.route('/billing', methods=['GET', 'POST'])
@login_required
def route_billing():
    return billing()

@app.route('/customer', methods=['GET', 'POST'])
@login_required
def route_customer():
    return customer()

@app.route('/virtual', methods=['GET', 'POST'])
@login_required
def route_virtual():
    return virtual()

@app.route('/rtl', methods=['GET', 'POST'])
@login_required
def route_rtl():
    return rtl()

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def route_profile():
    return profile()
