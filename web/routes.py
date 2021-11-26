from main import app, db
from flask import Blueprint, render_template, request, jsonify
from models import SSHLog, HTTPLog
from datetime import datetime
import json
import re

#from web.models import HTTPLog
#pattern = "\b(?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9];))\b"


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


@app.route('/api/ssh', methods=['GET', 'POST'])  # API-SSH ENDPOINT PAGE
def api_ssh():
    if request.method == 'POST':
        print(request.json)
        for loge in json.loads(request.json):
            print(loge)
            ip = loge.get("ip") 
            user = loge.get("username")
            pswd = loge.get("password")
            login = SSHLog(user=user, ip=ip, password=pswd, created_time=datetime.now())
            db.session.add(login)
        #db.session.query(SSHLog).delete()
        #db.session.commit()
        return request.json
    else:
        resp = SSHLog.query.all()
        print(resp)
        return jsonify([i.serialize for i in resp])

    #return render_template("api/ssh.html", values=log.query.all())
    


@app.route('/api/http', methods=['GET', 'POST'])  # API-HTTP ENDPOINT PAGE
def api_http():
    if request.method == 'POST':        
        print(request.json)
        for logs in json.loads(request.json):
            ip = logs.get("ip")
            httplogin = HTTPLog(ip=ip, created_time = datetime.now())
            db.session.add(httplogin)
            db.session.commit()
            print(httplogin)
        #db.session.query(HTTPLog).delete()
        #db.session.commit()
        return request.json
    else:
        resps = HTTPLog.query.all()
        print(resps)
        return jsonify([i.http_serialize for i in resps])
        



@app.route('/api/https', methods=['GET', 'POST'])  # API-HTTPS ENDPOINT PAGE
def api_https():
    return "WORKING ON THAT"
