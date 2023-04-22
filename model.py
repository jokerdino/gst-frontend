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
    office_code = db.Column(db.String)
    regional_code = db.Column(db.String, unique=True)
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
    regional_code = db.Column(db.String)#, db.ForeignKey("user.regional_code"))

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
    taxable_value= db.Column(db.String)
    total_tax= db.Column(db.String)
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
