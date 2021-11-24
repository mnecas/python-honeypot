from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, render_template, request
#from . import trace
from os import path


trace = Blueprint('trace', __name__)
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
    db.init_app(app)
    create_database(app)
    return app
