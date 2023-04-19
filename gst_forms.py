from flask_wtf import FlaskForm
from wtforms import DateField, StringField

class GSTInvoiceEditForm(FlaskForm):

    vendor = StringField("Vendor name")
    gst_number = StringField("Gst number")
    gst_invoice = StringField("GST invoice numebr")
    gst_invoice_date = DateField("GST invoice date")
    gst_amount = StringField("GST Amount")
    invoice_amount = StringField("Invoice amount")
