from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, render_template, request
from os import path
import argparse

app = Flask(__name__)
db = SQLAlchemy()
DB_NAME = "honeypot.db"
app.config['SECRET_KEY'] = 'aisjdausdhaisuvhaisghaiuehasdjansdhaxduiahiuzhaidsuhdsuahduiahyxdiahitgkahnjsfgkaasdijasidajsdoiajsdoasdasd'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'


def get_args():
    parser = argparse.ArgumentParser(
        description='Python honeypot web')
    parser.add_argument('--prod', action='store_true')
    return parser.parse_args()

from routes import *

if __name__ == '__main__':
    args = get_args()
    db.init_app(app)
    with app.app_context():
        db.create_all()
    if args.prod:
        app.run(host='0.0.0.0', port=80)
    else:
        app.run(debug=True)
