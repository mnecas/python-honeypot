from . import db
from sqlalchemy.sql import func


class log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    ip = db.Columnt(db.String(100))
    password = db.Column(db.String(100))
