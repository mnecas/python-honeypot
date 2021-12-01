from main import db
from sqlalchemy.sql import func

def dump_datetime(value):
    # This is function for converting the datetime to the json format
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

class SSHLog(db.Model):
    # The the sqlalchemy database structure
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    ip = db.Column(db.String(100))
    password = db.Column(db.String(100))
    created_time = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return f"SSHLog(id = {self.id}, user = {self.user}, ip = {self.ip}, password = {self.password}, created_time = {self.created_time})"
    # Serialization for the json dumps
    @property
    def serialize(self):
        return {
            'id': self.id,
            'ip': self.ip,
            'password': self.password,
            'user': self.user,
            'created_time': dump_datetime(self.created_time)
        }


class HTTPLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(100))
    created_time = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return f"HTTPLog(id = {self.id}, ip = {self.ip}, created_time = {self.created_time})"


    @property
    def http_serialize(self):
        return {
            'id': self.id,
            'ip': self.ip,
            'created_time': dump_datetime(self.created_time)
        }

class HTTPSLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(100))
    created_time = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return f"HTTPSLog(id = {self.id}, ip = {self.ip}, created_time = {self.created_time})"


    @property
    def https_serialize(self):
        return {
            'id': self.id,
            'ip': self.ip,
            'created_time': dump_datetime(self.created_time)
        }

class Honeypot(db.Model):
    # List of honeypots
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(100))
