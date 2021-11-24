from . import db
from sqlalchemy.sql import func






class SSHLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    ip = db.Column(db.String(100))
    password = db.Column(db.String(100))
    created_time = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return f"SSHLog(id = {self.id}, user = {self.user}, ip = {self.ip}, password = {self.password}, created_time = {self.created_time})"