from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Catalog(db.Model):
    # ID for this current title, internally.
    item_id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String, nullable=False)
    # ID for this title, in NUS.
    title_id = db.Column(db.String, nullable=False)
    latest_version = db.Column(db.Integer, nullable=False)


class Patches(db.Model):
    patch_id = db.Column(db.Integer, primary_key=True, unique=True)
    item_id = db.Column(db.Integer, db.ForeignKey("catalog.item_id"), nullable=False)
    content_id = db.Column(db.Integer, nullable=False)
