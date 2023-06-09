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

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String)
    office_code = db.Column(db.Integer)
    regional_code = db.Column(db.Integer, unique=True)
    password = db.Column(db.String)
    admin = db.Column(db.Boolean)
#    office = db.relationship("Office_code", backref=db.backref("office", uselist=False))

    def get_id(self):
        return str(self.id)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True


class Entries(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    office_code = db.Column(db.Integer)
    regional_code = db.Column(db.Integer)#, db.ForeignKey("user.regional_code"))

   # user = db.relationship("User", backref=db.backref("user", uselist=False))

    company_gstin= db.Column(db.String)
    purchaser = db.Column(db.String)
    match_result= db.Column(db.String)
    supplier_gstin= db.Column(db.String)
    supplier_name= db.Column(db.String)
    source= db.Column(db.String)
    verified= db.Column(db.String)
    business_unit= db.Column(db.String)
    doc_type= db.Column(db.String)
    doc_no= db.Column(db.String)
    doc_date= db.Column(db.String)
    return_period= db.Column(db.String)
    r1_filing_status= db.Column(db.String)
    r1_filing_date= db.Column(db.String)
    r3b_filing_status= db.Column(db.String)
    purchase_type= db.Column(db.String)
    revision= db.Column(db.String)
    original_doc_no= db.Column(db.String)
    original_doc_date= db.Column(db.String)
    place_of_supply= db.Column(db.String)
    rcm= db.Column(db.String)
    taxable_value= db.Column(db.Integer)
    total_tax= db.Column(db.Integer)
    doc_value= db.Column(db.String)
    gst_rate= db.Column(db.String)
    item_reference_no= db.Column(db.String)
    item_type= db.Column(db.String)
    item_description= db.Column(db.String)
    hsn_code= db.Column(db.String)
    item_taxable_value= db.Column(db.String)
    igst= db.Column(db.String)
    cgst= db.Column(db.String)
    sgst= db.Column(db.String)
    cess= db.Column(db.String)
    itc_eligible= db.Column(db.String)
    itc_ineligible_reason= db.Column(db.String)
    itc_claim_period= db.Column(db.String)
    itc_claim_percent = db.Column(db.String)
    itc_claim_status= db.Column(db.String)
    erp_ref_no= db.Column(db.String)
    erp_ref_date= db.Column(db.String)
    transaction_id= db.Column(db.String)
    transaction_date= db.Column(db.String)
    doc_label_1= db.Column(db.String)
    doc_label_2= db.Column(db.String)
    doc_label_3= db.Column(db.String)
    keywords= db.Column(db.String)
    reconciliation_notes= db.Column(db.String)
    group_id = db.Column(db.String)
    status = db.Column(db.String)

    def to_dict(self):
        return {
            'regional_code': self.regional_code,
            'office_code': self.office_code,
            'supplier_name': self.supplier_name,
            'supplier_gstin': self.supplier_gstin,
            'doc_no': self.doc_no,
            'doc_date': self.doc_date,
            'taxable_value': self.taxable_value,
            'total_tax': self.total_tax,
            'keywords': self.keywords,
            'id': self.id

            # voucher number
            # regional code, office code, vendor name, gst number,
            # gst invoice number, gst invoice date, gst invoice amount, gst tax amount
        }


class Cheques(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    office_code = db.Column(db.Integer)
    regional_code = db.Column(db.Integer)

    cheque_number = db.Column(db.String)
    cheque_date = db.Column(db.String)
    cheque_amount = db.Column(db.String)
    cheque_drawers_name = db.Column(db.String)
    file_upload = db.Column(db.String)
    cheque_status = db.Column(db.String)
    cheque_remarks = db.Column(db.String)
    def to_dict(self):
        return {
            'office_code': self.office_code,
            'regional_code': self.regional_code,
            'cheque_number': self.cheque_number,
            'cheque_date': self.cheque_date,
            'cheque_amount': self.cheque_amount,
            'cheque_drawers_name': self.cheque_drawers_name,
            'id': self.id

    }
