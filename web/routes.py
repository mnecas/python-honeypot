from main import app, db
from flask import Blueprint, render_template, request, jsonify
from models import SSHLog
from datetime import datetime
import json



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
            db.session.commit()
        return request.json
    else:
        resp = SSHLog.query.all()
        print(resp)
        return jsonify(resp)

    #return render_template("api/ssh.html", values=log.query.all())
    


@app.route('/api/http', methods=['GET', 'POST'])  # API-HTTP ENDPOINT PAGE
def api_http():
    return "WORKING ON THAT"


@app.route('/api/https', methods=['GET', 'POST'])  # API-HTTPS ENDPOINT PAGE
def api_https():
    return "WORKING ON THAT"
