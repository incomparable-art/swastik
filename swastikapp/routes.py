from swastikapp import *
from swastikapp.views.admin.account import login, signup, logout
from swastikapp.views.admin.dashboad import dashboard
from swastikapp.views.user.website import index



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
