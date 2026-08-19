from swastikapp import app
from swastikapp.views.user.website import index
from swastikapp.views.admin.account import login, signup, logout

from swastikapp.views.admin.dashboad import dashboard, virtual, rtl, profile

from swastikapp.views.admin.invoice import (
    billing, bill, invoice, delete_invoice, edit_invoice, add_invoice, generate_invoice_pdf, generate_invoice_pdf_by_id)

from swastikapp.views.admin.customer import (
    customer, add_customer, get_customer, get_customers, update_customer, delete_customer)

from flask_login import login_required

#####################################################################
#                           Admin Access                            #
#####################################################################
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def route_dashboard():
    return dashboard()

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

#################################################################################
#                                                                               #
#                              Authentication Routes                            #
#                                                                               #
#################################################################################
@app.route('/signup', methods=['GET', 'POST'])
def route_signup():
    return signup()

@app.route('/login', methods=['GET', 'POST'])
def route_admin_login():
    return login()

@app.route('/logout')
@login_required
def route_admin_logout():
    return logout()

#################################################################################
#                                                                               #
#                                Website Routes                                 #
#                                                                               #
#################################################################################
@app.route('/', methods=['GET', 'POST'])
def route_index():
    return index()

#################################################################################
#                                                                               #
#                                 Invoice Routes                                #
#                                                                               #
#################################################################################
@app.route('/billing', methods=['GET', 'POST'])
@login_required
def route_billing():
    return billing()

@app.route('/bill', methods=['GET', 'POST'])
@login_required
def route_bill():
    return bill()

@app.route('/invoice', methods=['GET', 'POST'])
@login_required
def route_invoice():
    return invoice()

@app.route('/edit-invoice/<invoice_id>', methods=['GET', 'POST'])
@login_required
def route_edit_invoice(invoice_id):
    return edit_invoice(invoice_id)

@app.route('/delete-invoice/<invoice_id>', methods=['GET', 'POST'])
@login_required
def route_delete_invoice(invoice_id):
    return delete_invoice(invoice_id)

@app.route('/add-invoice', methods=['GET', 'POST'])
@login_required
def route_add_invoice():
    return add_invoice()

@app.route('/generate-invoice-pdf', methods=['POST'])
@login_required
def route_generate_invoice_pdf():
    return generate_invoice_pdf()

@app.route('/generate-invoice-pdf/<invoice_id>', methods=['GET'])
@login_required
def route_generate_invoice_pdf_by_id(invoice_id):
    return generate_invoice_pdf_by_id(invoice_id)

#################################################################################
#                                                                               #
#                                 Customer Routes                               #
#                                                                               #
#################################################################################
@app.route('/customer', methods=['GET', 'POST'])
@login_required
def route_customer():
    return customer()

@app.route('/api/add-customer', methods=['POST'])
@login_required
def route_add_customer():
    return add_customer()

@app.route('/api/get-customers', methods=['GET'])
@login_required
def route_get_customers():
    return get_customers()

@app.route('/api/update-customer', methods=['POST'])
@login_required
def route_update_customer():
    return update_customer()

@app.route('/api/get-customer/<customer_id>', methods=['GET'])
@login_required
def route_get_customer(customer_id):
    return get_customer(customer_id)

@app.route('/api/delete-customer/<customer_id>', methods=['DELETE'])
@login_required
def route_delete_customer(customer_id):
    return delete_customer(customer_id)
