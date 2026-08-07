from swastikapp.database import MongoDatabase

from flask import render_template, request, flash, redirect, url_for

def dashboard():
    with MongoDatabase() as mongo:
        # Fetch all users as User objects
        all_users = mongo.get_all_users()
        templateData = {'users': all_users}
        # for user in all_users:
        #     print(f"ID: {user.id} | Name: {user.name} | Role: {user.role} | Active: {user.is_active}")

    return render_template("admin/dashboard.html", **templateData)

def tables():
    templateData = {'page': "Table"}
    return render_template("admin/tables.html", **templateData)

def billing():
    templateData = {'page': "Billing"}
    return render_template("admin/billing.html", **templateData)

def virtual():
    templateData = {'page': "Virtual Reality"}
    return render_template("admin/virtual.html", **templateData)

def rtl():
    templateData = {'page': "RTL"}
    return render_template("admin/rtl.html", **templateData)

def profile():
    templateData = {'page': "Profile"}
    return render_template("admin/profile.html", **templateData)
