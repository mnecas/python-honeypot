from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, render_template, request
#from . import trace
from os import path


trace = Blueprint('trace', __name__)


@trace.route('/', methods=['GET'])  # HOME PAGE
def home():
    return render_template("home.html")


@trace.route('/ssh', methods=['GET'])  # SSH PAGE
def ssh():
    return render_template("ssh.html")


@trace.route('/http', methods=['GET'])  # HTTP PAGE
def http():
    return render_template("http.html")


@trace.route('/https', methods=['GET'])  # HTTPS PAGE
def https():
    return render_template("https.html")


db = SQLAlchemy()
DB_NAME = "honeypot.db"


def create_database(tt):
    if not path.exists('web/' + DB_NAME):
        db.create_all(app=tt)
        print('Created Database!')


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'aisjdausdhaisuvhaisghaiuehasdjansdhaxduiahiuzhaidsuhdsuahduiahyxdiahitgkahnjsfgkaasdijasidajsdoiajsdoasdasd'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.register_blueprint(trace, url_prefix='/')

    create_database(app)
    from models import log
    return app
