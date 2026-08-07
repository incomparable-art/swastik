from swastikapp import app
from swastikapp.views.admin.account import login, signup, logout
from swastikapp.views.admin.dashboad import dashboard, tables, billing, virtual, rtl, profile
from swastikapp.views.user.website import index
from flask_login import login_required


@app.route('/signup', methods=['GET', 'POST'])
def route_signup():
    return signup()

@app.route('/login', methods=['GET', 'POST'])
def route_admin_login():
    return login()

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def route_dashboard():
    return dashboard()

@app.route('/logout')
@login_required
def route_admin_logout():
    return logout()

@app.route('/', methods=['GET', 'POST'])
def route_index():
    return index()

@app.route('/tables', methods=['GET', 'POST'])
def route_tables():
    return tables()

@app.route('/billing', methods=['GET', 'POST'])
def route_billing():
    return billing()

@app.route('/virtual', methods=['GET', 'POST'])
def route_virtual():
    return virtual()

@app.route('/rtl', methods=['GET', 'POST'])
def route_rtl():
    return rtl()

@app.route('/profile', methods=['GET', 'POST'])
def route_profile():
    return profile()
