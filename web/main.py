from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, render_template, request
from os import path

global app
global db
app = Flask(__name__)
db = SQLAlchemy()
DB_NAME = "honeypot.db"
app.config['SECRET_KEY'] = 'aisjdausdhaisuvhaisghaiuehasdjansdhaxduiahiuzhaidsuhdsuahduiahyxdiahitgkahnjsfgkaasdijasidajsdoiajsdoasdasd'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'


from routes import *

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
