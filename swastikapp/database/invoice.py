from flask_login import UserMixin
from datetime import datetime

# -------------------------------------------------------------#
# 1. Flask-Login Customer Model (Data Object Wrapper)
# -------------------------------------------------------------
class Invoice(UserMixin):
    def __init__(self, invoice_doc: dict):
        self.id = str(invoice_doc['_id'])
        self.invoice_no = invoice_doc.get('invoice_no', '')
        self.invoice_date = invoice_doc.get('invoice_date', '')
        self.place_of_supply = invoice_doc.get('place_of_supply', '')
        self.reverse_charge = invoice_doc.get('reverse_charge', '')
        self.rr_no = invoice_doc.get('rr_no', '')
        self.transport = invoice_doc.get('transport', '')
        self.vehicle_no = invoice_doc.get('vehicle_no', '')
        self.station = invoice_doc.get('station', '')
        self.eway_bill = invoice_doc.get('eway_bill', '')
        self.status = invoice_doc.get('status', '')
        self.buyer_name = invoice_doc.get('buyer_name', '')
        self.buyer_address = invoice_doc.get('buyer_address', '')
        self.buyer_gstin = invoice_doc.get('buyer_gstin', '')
        self.items = invoice_doc.get('items', '')
        self.taxtype = invoice_doc.get('taxtype', '')
        self.roundOff = invoice_doc.get('roundOff', '')
        self.taxable_amount = invoice_doc.get('taxable_amount', '')
        self.igst_amount = invoice_doc.get('igst_amount', '')
        self.total_tax = invoice_doc.get('total_tax', '')
        self.gst_amount = invoice_doc.get('gst_amount', '')
        self.grand_total = invoice_doc.get('grand_total', '')
        self.amount_in_words = invoice_doc.get('amount_in_words', '')
        self.user = invoice_doc.get('email', '')
        self.created_date = invoice_doc.get('created_date', '')
        self.updated_date = invoice_doc.get('updated_date', '')

    def to_dict(self):
        """Converts the Customer instance attributes into a JSON-serializable dictionary."""
        return {
            'id': self.id,
            'invoice_no': self.invoice_no,
            'invoice_date': self.invoice_date,
            'place_of_supply': self.place_of_supply,
            'reverse_charge': self.reverse_charge,
            'rr_no': self.rr_no,
            'transport': self.transport,
            'vehicle_no': self.vehicle_no,
            'station': self.station,
            'eway_bill': self.eway_bill,
            'status': self.status,
            'buyer_name': self.buyer_name,
            'buyer_address': self.buyer_address,
            'buyer_gstin': self.buyer_gstin,
            'items': self.items,
            'taxtype': self.taxtype,
            'roundOff': self.roundOff,
            'taxable_amount': self.taxable_amount,
            'igst_amount': self.igst_amount,
            'total_tax': self.total_tax,
            'gst_amount': self.gst_amount,
            'grand_total': self.grand_total,
            'amount_in_words': self.amount_in_words,
            'user': self.user,
            'created_date': self.created_date.isoformat() if isinstance(self.created_date, datetime) else str(self.created_date),
            'updated_date': self.updated_date.isoformat() if isinstance(self.updated_date, datetime) else str(self.updated_date)
        }


