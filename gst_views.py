from datetime import datetime

from sqlalchemy import cast, String
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from model import Entries, User, db
from gst_forms import GSTInvoiceEditForm, LoginForm

from gst_input import upload_details

@login_required
def home_page():
    return render_template("home.html")

@login_required
def invoices_pending():
    return render_template('list_pending.html', source="/api/data/pending")

@login_required
def invoices_completed():
    return render_template('list_pending.html', source="/api/data/completed")

@login_required
def upload():
    if request.method == "POST":
        upload_file = request.files.get("file")
#        convert_input(upload_file)
       # flash("GST invoice data has been received. Processing the input file..")
        upload_details(upload_file)
        flash("GST invoice data has been processed and added to database.")
    return render_template("upload.html")

def data_pending():
    return data("To be updated")

def data_completed():
    return data("Updated")

def data(status):

    if not current_user.admin:
        entries = (
                Entries.query.filter(Entries.regional_code == current_user.regional_code)
                .filter(Entries.status == status)
                )
        entries_count = entries.count()
    else:
        entries = (
                Entries.query.filter(Entries.status == status)
                )
        entries_count = entries.count()
    # search filter
    # TODO: add more parameters for searching
    search = request.args.get('search[value]')
    if search:
        entries = entries.filter(db.or_(
            Entries.supplier_name.ilike(f'%{search}%'),
            cast(Entries.office_code, String).like(f'%{search}%')
        ))

    total_filtered = entries.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(Entries, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        entries = entries.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    entries = entries.offset(start).limit(length)

    # response
    return {'data': [entry.to_dict() for entry in entries],
            'recordsFiltered': total_filtered,
            'recordsTotal': entries_count,
            'draw': request.args.get('draw', type=int),}


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
        return redirect(url_for("invoices_pending"))

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
        user = db.session.query(User).filter(User.username == username).first()
        if user is not None:
            password = form.data["password"]

            #if check_password_hash(user.password, password):
            if user.password == password:
                login_user(user)

                next_page = request.args.get("next", url_for("home_page"))
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
