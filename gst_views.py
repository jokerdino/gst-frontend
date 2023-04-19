from datetime import datetime

from flask import redirect, render_template, request, url_for


from model import Entries
from gst_forms import GSTInvoiceEditForm

def pending_gst_corrections():
    from server import db
    entries = Entries.query.all()
    return render_template("list_pending.html",entries=entries)


def edit_entries(invoice_key):
    from server import db
    entry = Entries.query.get_or_404(invoice_key)
    form = GSTInvoiceEditForm()
    if form.validate_on_submit():
        entry.supplier_gst_number = form.data['gst_number']
        entry.gst_invoice = form.data['gst_invoice']
        entry.gst_date  = form.data['gst_invoice_date']
        db.session.commit()
        return redirect(url_for("pending_gst_corrections"))

    form.vendor.data = entry.vendor
    form.gst_amount.data = entry.gst_value
    form.gst_invoice.data = entry.gst_invoice
    form.invoice_amount.data = entry.invoice_value
    form.gst_number.data = entry.supplier_gst_number
    try:
        form.gst_invoice_date.data = datetime.strptime(entry.gst_date, '%Y-%m-%d %H:%M:%S') if entry.gst_date else ""
    #form.gst_invoice_date.data = entry.gst_date
    except ValueError as e:
        form.gst_invoice_date.data = datetime.strptime(entry.gst_date, "%Y-%m-%d") if entry.gst_date else ""
    return render_template("gst_entry.html", form=form, entry=entry)
