from flask import Flask

from flask_login import LoginManager
from flask_migrate import Migrate
from waitress import serve

from model import Entries, db
import gst_views

migrate = Migrate()
lm = LoginManager()

def create_app():

    app = Flask(__name__)

    app.config.from_object("settings")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///gstinvoices.sqlite"

    app.add_url_rule("/", view_func=gst_views.pending_gst_corrections)
    app.add_url_rule("/<int:invoice_key>/edit", view_func=gst_views.edit_entries, methods=["GET", "POST"])
    db.init_app(app)
    migrate.init_app(app,db)
    #app.config[""]
    return app


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=8000)


