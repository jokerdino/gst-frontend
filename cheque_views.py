from datetime import datetime

from sqlalchemy import cast, String
from flask import flash, redirect, render_template, request, send_file, url_for
from flask_login import current_user, login_required, login_user, logout_user

from model import User, Cheques
from cheque_forms import ChequeEditform
from cheque_input import upload_cheque_entries


def list_unreconciled(source):
    source = f"/api/cheque_data/{source}"
#    print(source)
    if request.method == "GET":

        return render_template("cheques_unreconciled.html", source = source)
    else:
        from server import db
        form_cheque_keys = request.form.getlist("cheque_keys")
        for form_cheque_key in form_cheque_keys:
            print(form_cheque_key)
            cheque = Cheques.query.get_or_404(form_cheque_key)
            cheque.cheque_status = "agreed"
            #cheque.commit()
            db.session.commit()
        return render_template("cheques_unreconciled.html", source = source)


#def list_agreed():
#    return render_template("cheques_unreconciled.html", source="/api/cheque_data/Agreed")
#
#def cheques_agreed():
#    return cheque_data("Agreed")
#
## api for unreconciled cheques
#def cheques_unreconciled():
#    return cheque_data("Unreconciled")

def cheque_data(status):
    from server import db
    cheque_entries = Cheques.query.filter(Cheques.cheque_status == status)

    cheques_count = cheque_entries.count()

    # search filter
    # TODO: enable more parameters for searching
    search = request.args.get('search[value]')
    if search:
        cheque_entries = cheque_entries.filter(db.or_(
            cast(Cheques.office_code, String).like(f'%{search}%')
            ))

    total_filtered = cheque_entries.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(Cheques, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        cheque_entries = cheque_entries.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    cheque_entries = cheque_entries.offset(start).limit(length)

    return {'data': [cheque.to_dict() for cheque in cheque_entries],
            'recordsFiltered': total_filtered,
            'recordsTotal': cheques_count,
            'draw': request.args.get('draw', type=int),
            }

def edit_cheque_entries(cheque_key):
    form = ChequeEditform()
    from server import db
    entry = Cheques.query.get_or_404(cheque_key)
    if form.validate_on_submit():
        entry.cheque_status = form.data['cheque_status']
        entry.cheque_remarks = form.data['cheque_remarks']
        db.session.commit()
        return redirect(url_for("list_unreconciled", source="Unreconciled"))

    form.cheque_status.data = entry.cheque_status
    form.cheque_remarks.data= entry.cheque_remarks
    return render_template("cheque_entry.html", form=form, entry=entry)

def download_format():
    return send_file("format_cheque.xlsx",download_name="cheque_upload_format.xlsx", as_attachment=True)

def cheque_upload():

    if request.method == "POST":
        upload_file = request.files.get("file")
        upload_cheque_entries(upload_file)
    return render_template("cheque_upload.html")
