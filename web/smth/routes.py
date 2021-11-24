from __main__ import app
from flask import Blueprint, render_template, request

@app.route('/', methods=['GET'])  # HOME PAGE
def home():
    return render_template("home.html")


@app.route('/ssh', methods=['GET'])  # SSH PAGE
def ssh():
    return render_template("ssh.html")


@app.route('/http', methods=['GET'])  # HTTP PAGE
def http():
    return render_template("http.html")


@app.route('/https', methods=['GET'])  # HTTPS PAGE
def https():
    return render_template("https.html")
