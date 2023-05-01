from flask_wtf import FlaskForm
from wtforms import BooleanField, RadioField, StringField
from wtforms.validators import DataRequired, Optional


class ChequeEditform(FlaskForm):
    ...

    cheque_status_reasons = [("agreed","Agreed"), ("office_mismatch","Does not belong to our office"),("amount_mismatch", "Amount mismatch"),("others","Others")]
    cheque_status = RadioField("Agreed or not", choices=cheque_status_reasons, validators=[DataRequired()])
    cheque_remarks = StringField("Enter remarks:", validators=[Optional()])
    confirm_update = BooleanField("Please confirm that the changes have been made", validators=[DataRequired()])
    # if cheque entry agreed, status will become reconciled

    # if cheque entry not agreed, need to collect reasons for it

    # not belong to office
        # enable option to change office code -- move it to regional office ??
    # amount differs
    # others - enable text area


