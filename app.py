import config
from flask import Flask
from flask_migrate import Migrate
from models import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = config.secret_key
app.config["OIDC_CLIENT_SECRETS"] = config.oidc_client_secrets_json
app.config["OIDC_SCOPES"] = "openid profile"
app.config["OIDC_OVERWRITE_REDIRECT_URI"] = config.oidc_redirect_uri


db.init_app(app)

migrate = Migrate(app, db)

with app.app_context():
    # Ensure our database is present.
    db.create_all()


import catalog
