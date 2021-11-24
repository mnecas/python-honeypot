from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, render_template, request
from os import path

global db
db = SQLAlchemy()
DB_NAME = "honeypot.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'aisjdausdhaisuvhaisghaiuehasdjansdhaxduiahiuzhaidsuhdsuahduiahyxdiahitgkahnjsfgkaasdijasidajsdoiajsdoasdasd'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    db.create_all(app=app)
    return app
