from flask import Flask

from flask_login import LoginManager
from flask_migrate import Migrate
from waitress import serve

from model import User, db
import gst_views

migrate = Migrate()
lm = LoginManager()

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():

    app = Flask(__name__)

    app.config.from_object("settings")
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://barneedhar:barneedhar@localhost:5432/flask_db"
    #app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///gstinvoices.sqlite"

    app.add_url_rule("/", view_func=gst_views.login_page, methods=["GET", "POST"])
    app.add_url_rule("/home", view_func=gst_views.home_page, methods=["GET", "POST"])
    app.add_url_rule("/user/logout", view_func=gst_views.logout_page)
    app.add_url_rule("/api/data/pending", view_func=gst_views.data_pending)
    app.add_url_rule("/api/data/completed", view_func=gst_views.data_completed)
    # app.add_url_rule("/", view_func=gst_views.pending_gst_corrections)
    app.add_url_rule("/pending", view_func=gst_views.invoices_pending)
    app.add_url_rule("/completed", view_func=gst_views.invoices_completed)
    app.add_url_rule("/<int:invoice_key>/edit", view_func=gst_views.edit_entries, methods=["GET", "POST"])
    app.add_url_rule("/upload", view_func=gst_views.upload, methods=["POST", "GET"])
    lm.init_app(app)
    #lm.login_view = "login_page"

    db.init_app(app)
    migrate.init_app(app,db)
    #app.config[""]
    return app


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=8000)


