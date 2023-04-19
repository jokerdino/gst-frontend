from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_login import UserMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)


db = SQLAlchemy(metadata=metadata)

class Entries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    office_code = db.Column(db.Integer)

    vendor = db.Column(db.String)
    supplier_gst_number = db.Column(db.String)
    gst_invoice = db.Column(db.String)
    gst_date = db.Column(db.String)
    invoice_value = db.Column(db.String)
    gst_value = db.Column(db.String)

