from swastikapp.database.db import MongoDatabase
from flask_login import current_user
from flask import render_template, request, flash, redirect, url_for, jsonify, make_response
from datetime import datetime
import pdfkit


def dashboard():
    with MongoDatabase() as mongo:
        # Fetch all users as User objects
        all_users = mongo.get_all_users()
        invoices = mongo.get_all_invoices()
        clients = mongo.get_all_customers()
        total_tax, taxable_amount,  grand_total = 0, 0, 0
        d_total_tax, d_taxable_amount,  d_grand_total = 0, 0, 0

        if len(invoices)>0:
            for invoice in invoices:
                if invoice.status == "updated" or invoice.status == "created":
                    total_tax += int(float(invoice.total_tax))
                    taxable_amount += int(float(invoice.taxable_amount))
                    grand_total += int(float(invoice.grand_total))
                elif invoice.status == "deleted":
                    d_total_tax += int(float(invoice.total_tax))
                    d_taxable_amount += int(float(invoice.taxable_amount))
                    d_grand_total += int(float(invoice.grand_total))

            p_total_tax = int(d_total_tax*100/total_tax)
            p_taxable_amount = int(d_taxable_amount*100/taxable_amount)
            p_grand_total = int(d_grand_total*100/grand_total)

        templateData = {
            'page': "Dashboard", 'users': all_users, 'user_count': len(all_users),
            'invoices': invoices, 'taxable_amount':taxable_amount, 'total_tax':total_tax,
            'grand_total': grand_total,'d_total_tax':d_total_tax, 'd_taxable_amount':d_taxable_amount,
            'd_grand_total': d_grand_total, 'p_total_tax':p_total_tax, 'p_taxable_amount':p_taxable_amount,
            'p_grand_total': p_grand_total, 'client_count': len(clients),
        }

    return render_template("admin/dashboard.html", **templateData)

def virtual():
    templateData = {'page': "Virtual Reality"}
    return render_template("admin/virtual.html", **templateData)

def rtl():
    templateData = {'page': "RTL"}
    return render_template("admin/rtl.html", **templateData)

def profile():
    templateData = {'page': "Profile"}
    return render_template("admin/profile.html", **templateData)
