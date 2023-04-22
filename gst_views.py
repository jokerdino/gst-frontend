from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from model import Entries, User
from gst_forms import GSTInvoiceEditForm, LoginForm

@login_required
def pending_gst_corrections():
    #from server import db

    # TODO: server side pagination pending
    if not current_user.admin:
        entries = (
                Entries.query.filter(Entries.regional_code == current_user.regional_code)
                .filter(Entries.status != "Updated")
                .order_by(Entries.total_tax).paginate(page=1,per_page=2000)
                )
    else:
        entries = (
                Entries.query.filter(Entries.status != "Updated")
                .order_by(Entries.total_tax).paginate(page=1,per_page=2000)
                )
    return render_template("list_pending.html",entries=entries)

def completed_gst_corrections():
    ...

def upload_page():
    ...

def download_page():
    ...

def admin_dashboard():
    # to see statistics
    ...

def admin_user_dashboard():
    # to see when the user last logged in
    ...

@login_required
def edit_entries(invoice_key):
    from server import db
    entry = Entries.query.get_or_404(invoice_key)
    form = GSTInvoiceEditForm()
    if form.validate_on_submit():
        entry.supplier_gstin = form.data['gst_number']
        entry.doc_no = form.data['gst_invoice']
        entry.doc_date  = form.data['gst_invoice_date']
        entry.status = "Updated"
        db.session.commit()
        return redirect(url_for("pending_gst_corrections"))

    form.vendor.data = entry.supplier_name
    form.gst_amount.data = entry.total_tax
    form.gst_invoice.data = entry.doc_no
    form.invoice_amount.data = entry.taxable_value
    form.gst_number.data = entry.supplier_gstin
    try:
        form.gst_invoice_date.data = datetime.strptime(entry.doc_date, '%Y-%m-%d %H:%M:%S') if entry.doc_date else ""
    #form.gst_invoice_date.data = entry.gst_date
    except ValueError as e:
        form.gst_invoice_date.data = datetime.strptime(entry.doc_date, "%Y-%m-%d") if entry.doc_date else ""
    return render_template("gst_entry.html", form=form, entry=entry)

def login_page():
    if current_user.is_authenticated:
        return redirect(url_for("pending_gst_corrections"))
    form = LoginForm()

    from server import db

    if form.validate_on_submit():
        username = form.data["username"]
        user = db.session.query(User).filter(User.office_code == username).first()
        if user is not None:
            password = form.data["password"]

            #if check_password_hash(user.password, password):
            if user.password == password:
                login_user(user)

                next_page = request.args.get("next", url_for("pending_gst_corrections"))
                return redirect(next_page)
            else:
                flash("Invalid credentials.")
        else:
            flash("Invalid credentials.")
    return render_template("login.html", form=form)


def logout_page():
    logout_user()
    # flash("You have logged out.")
    return redirect(url_for("login_page"))
