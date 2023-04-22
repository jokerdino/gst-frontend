from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, PasswordField, StringField
from wtforms.validators import DataRequired, Optional
class GSTInvoiceEditForm(FlaskForm):

    vendor = StringField("Vendor name")
    gst_number = StringField("Gst number")
    gst_invoice = StringField("GST invoice numebr")
    gst_invoice_date = DateField("GST invoice date")
    gst_amount = StringField("GST Amount")
    invoice_amount = StringField("Invoice amount")
    confirm_update = BooleanField("Please confirm that the changes have been made", validators=[DataRequired()])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
