from swastikapp.database.db import MongoDatabase
from flask import render_template, request, make_response, redirect, url_for
import pdfkit
from datetime import datetime

def billing():
    with MongoDatabase() as mongo:
        invoices = mongo.get_all_invoices()
        total_tax = 0
        taxable_amount = 0
        for invoice in invoices:
            total_tax += int(float(invoice.total_tax))
            taxable_amount += int(float(invoice.taxable_amount))

    templateData = {'page': "Billing", "invoices": invoices, "total_tax": total_tax, "taxable_amount": taxable_amount}
    return render_template("admin/billing.html", **templateData)

def bill():
    return render_template("admin/invoice/bill.html")

def tables():
    with MongoDatabase() as mongo:
        all_users = mongo.get_all_users()

    templateData = {'page': "table", 'users': all_users}
    return render_template("admin/tables.html", **templateData)

def invoice():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    filter_query = {}

    with MongoDatabase() as mongo:
        pagination = mongo.get_paginated_invoices(
            page=page,
            per_page=per_page,
            filter_query=filter_query
        )
    templateData = {
        'page': "invoice", 'pagination': pagination
    }
    return render_template("admin/invoice/invoice.html", **templateData)

def delete_invoice(invoice_id):
    with MongoDatabase() as mongo:
        mongo.update_invoice_status(invoice_id=invoice_id, new_status="deleted")

    return redirect(url_for('route_invoice'))

def edit_invoice(invoice_id):
    if request.method == 'POST':

        # 1. Parse List of Items from Form
        descs = request.form.getlist('item_desc[]')
        hsns = request.form.getlist('item_hsn[]')
        qtys = request.form.getlist('item_qty[]')
        units = request.form.getlist('item_unit[]')
        rates = request.form.getlist('item_rate[]')
        amts = request.form.getlist('item_amt[]')

        items = []
        for i in range(len(descs)):
            items.append({
                'desc': descs[i],
                'hsn': hsns[i],
                'qty': qtys[i],
                'unit': units[i],
                'rate': rates[i],
                'amount': amts[i]
            })

        tax_type = request.form.get('taxtype')
        total_tax = float(request.form.get('total_tax'))
        igst_amount = 0
        gst_amount = 0

        if tax_type == "CGST/SGST":
            igst_amount = 0
            gst_amount = total_tax / 2
        else:
            gst_amount = 0
            igst_amount = total_tax

        # 2. Package all invoice data
        templateData = {
            'invoice_no': request.form.get('invoice_no'),
            'invoice_date': request.form.get('invoice_date'),
            'place_of_supply': request.form.get('place_of_supply'),
            'reverse_charge': request.form.get('reverse_charge'),
            'rr_no': request.form.get('rr_no'),
            'transport': request.form.get('transport'),
            'vehicle_no': request.form.get('vehicle_no'),
            'station': request.form.get('station'),
            'eway_bill': request.form.get('eway_bill'),
            'status': 'updated',
            'buyer_name': request.form.get('buyer_name'),
            'buyer_address': request.form.get('buyer_address'),
            'buyer_gstin': request.form.get('buyer_gstin'),
            'items': items,
            'taxtype': request.form.get('taxtype'),
            'roundOff': request.form.get('roundOff'),
            'taxable_amount': request.form.get('taxable_amount'),
            'igst_amount': igst_amount,
            'total_tax': total_tax,
            'gst_amount': gst_amount,
            'grand_total': request.form.get('grand_total'),
            'amount_in_words': request.form.get('amount_in_words'),
            'updated_date': datetime.now().strftime("%a %b %d %H:%M:%S %Y"),
        }

        # Save to MongoDB
        with MongoDatabase() as mongo:
            db = mongo.get_invoice_by_id(invoice_id)
            templateData['created_date'] = db.created_date
            success = mongo.update_invoice(id=invoice_id, data=templateData)

        # 3. Render HTML template with dynamic data
        rendered_html = render_template('admin/invoice/invoice_pdf_template.html', **templateData)

        # 4. Generate PDF from HTML
        pdf = pdfkit.from_string(rendered_html, False)

        # 5. Return as Downloadable PDF Response
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename=Invoice_{templateData["invoice_no"]}.pdf'
        return response

    with MongoDatabase() as mongo:
        with MongoDatabase() as mongo:
            invoice = mongo.get_invoice_by_id(invoice_id)
            customers = mongo.get_all_customers()

    templateData = {'page': "invoice", 'invoice': invoice, 'customers': customers}
    return render_template("admin/invoice/edit-invoice.html", **templateData)

def add_invoice():
    with MongoDatabase() as mongo:
        next_invoice_no = mongo.get_next_invoice_number_from_last()
        customers = mongo.get_all_customers()

        templateData = {'page': "dashboard", 'invoice_no': next_invoice_no, "customers": customers}
    return render_template("admin/invoice/add-invoice.html", **templateData)

def generate_invoice_pdf():
    # 1. Parse List of Items from Form
    descs = request.form.getlist('item_desc[]')
    hsns = request.form.getlist('item_hsn[]')
    qtys = request.form.getlist('item_qty[]')
    units = request.form.getlist('item_unit[]')
    rates = request.form.getlist('item_rate[]')
    amts = request.form.getlist('item_amt[]')

    items = []
    for i in range(len(descs)):
        items.append({
            'desc': descs[i],
            'hsn': hsns[i],
            'qty': qtys[i],
            'unit': units[i],
            'rate': rates[i],
            'amount': amts[i]
        })

    tax_type = request.form.get('taxtype')
    total_tax = float(request.form.get('total_tax'))
    igst_amount = 0
    gst_amount = 0

    if tax_type == "CGST/SGST":
        igst_amount = 0
        gst_amount = total_tax / 2
    else:
        gst_amount = 0
        igst_amount = total_tax

    # 2. Package all invoice data
    templateData = {
        'invoice_no': request.form.get('invoice_no'),
        'invoice_date': request.form.get('invoice_date'),
        'place_of_supply': request.form.get('place_of_supply'),
        'reverse_charge': request.form.get('reverse_charge'),
        'rr_no': request.form.get('rr_no'),
        'transport': request.form.get('transport'),
        'vehicle_no': request.form.get('vehicle_no'),
        'station': request.form.get('station'),
        'eway_bill': request.form.get('eway_bill'),
        'buyer_name': request.form.get('buyer_name'),
        'buyer_address': request.form.get('buyer_address'),
        'buyer_gstin': request.form.get('buyer_gstin'),
        'items': items,
        'taxtype':request.form.get('taxtype'),
        'roundOff':request.form.get('roundOff'),
        'taxable_amount': request.form.get('taxable_amount'),
        'igst_amount': igst_amount,
        'total_tax': total_tax,
        'gst_amount': gst_amount,
        'grand_total': request.form.get('grand_total'),
        'amount_in_words': request.form.get('amount_in_words'),
        'created_date': datetime.now().strftime("%a %b %d %H:%M:%S %Y"),
        'updated_date': datetime.now().strftime("%a %b %d %H:%M:%S %Y"),
    }

    # Save to MongoDB
    with MongoDatabase() as mongo:
        mongo.db.invoices.insert_one(templateData)

    # 3. Render HTML template with dynamic data
    rendered_html = render_template('admin/invoice/invoice_pdf_template.html', **templateData)

    # 4. Generate PDF from HTML
    pdf = pdfkit.from_string(rendered_html, False)

    # 5. Return as Downloadable PDF Response
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=Invoice_{templateData["invoice_no"]}.pdf'
    return response

def generate_invoice_pdf_by_id(invoice_id):
    with MongoDatabase() as mongo:
        invoice = mongo.get_invoice_by_id(invoice_id)
    templateData = {"invoice": invoice}
        # 3. Render HTML template with dynamic data
    rendered_html = render_template('admin/invoice/invoice_pdf_template_by_id.html', **templateData)

    # 4. Generate PDF from HTML
    pdf = pdfkit.from_string(rendered_html, False)

    # 5. Return as Downloadable PDF Response
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=Invoice_{invoice.invoice_no}.pdf'
    return response
