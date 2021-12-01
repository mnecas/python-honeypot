
from main import app, db
from flask import render_template, request, jsonify, redirect
from models import SSHLog, HTTPLog, HTTPSLog, Honeypot
from datetime import datetime
from utils import add_host, remove_all_host
import json
import ansible_runner
import os
import socket


@app.route('/', methods=['GET'])  # HOME PAGE
def home():
    honeypots = Honeypot.query.all()
    return render_template("home.html", honeypots=honeypots)


@app.route('/add', methods=['GET', 'POST'])  # HOME PAGE
def add_server():
    if request.method == 'GET':
        return render_template("add_server.html")
    if request.method == 'POST':
        user_ip = request.form.get('ip')
        if user_ip:
            # Cleanup all host before adding the new one so the playbook runs on just one host
            remove_all_host()
            # Add host on which the playbook wil run
            add_host(user_ip)

            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)

            r = ansible_runner.run(
                private_data_dir=os.path.join(os.path.dirname(os.path.abspath(
                    ".")), 'honeypot', 'deploy'),
                playbook='honeypot-setup.yml',
                extravars={
                    "server_ip": local_ip
                }
            )
            if r.rc == 0:
                honeypot = Honeypot(hostname=user_ip)
                db.session.add(honeypot)
                db.session.commit()
                return redirect('/')
            if r.rc == 4:
                return render_template("add_server.html", warning="Could not connect to the server.")
            return render_template("add_server.html", warning="Some error in setup.")


@app.route('/del', methods=['GET'])  # SSH PAGE
def del_server():
    hon_id = request.args.get('id', default=1, type=int)
    honeypot = Honeypot.query.get(hon_id)
    if honeypot:
        # Cleanup all host before adding the new one so the playbook runs on just one host
        remove_all_host()
        # Add host on which the playbook wil run and change ansible_port to 6000
        add_host(honeypot.hostname, 6000)

        r = ansible_runner.run(
            private_data_dir=os.path.join(os.path.dirname(os.path.abspath(
                ".")), 'honeypot', 'deploy'),
            playbook='honeypot-cleanup.yml'
        )
        if r.rc == 0:
            u = db.session.get(Honeypot, honeypot.id)
            db.session.delete(u)
            db.session.commit()
    return redirect('/')


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
            time = loge.get("time")
            login = SSHLog(user=user, ip=ip, password=pswd,
                           created_time=datetime.fromtimestamp(float(str(time))))
            db.session.add(login)
            db.session.commit()
        # db.session.query(SSHLog).delete()
        # db.session.commit()
        return request.json
    else:
        resp = SSHLog.query.all()
        print(resp)
        return jsonify([i.serialize for i in resp])

    # return render_template("api/ssh.html", values=log.query.all())


@app.route('/api/http', methods=['GET', 'POST'])  # API-HTTP ENDPOINT PAGE
def api_http():
    if request.method == 'POST':
        print(request.json)
        for logs in json.loads(request.json):
            ip = logs.get("ip")
            time = logs.get("time")
            httplogin = HTTPLog(ip=ip, created_time=datetime.fromtimestamp(float(str(time))))
            db.session.add(httplogin)
            db.session.commit()
            print(httplogin)
        # db.session.query(HTTPLog).delete()
        # db.session.commit()
        return request.json
    else:
        resps = HTTPLog.query.all()
        print(resps)
        return jsonify([i.http_serialize for i in resps])


@app.route('/api/https', methods=['GET', 'POST'])  # API-HTTPS ENDPOINT PAGE
def api_https():
    if request.method == 'POST':
        print(request.json)
        for logs in json.loads(request.json):
            ip = logs.get("ip")
            httpslogin = HTTPSLog(ip=ip, created_time=datetime.fromtimestamp(float(str(time))))
            db.session.add(httpslogin)
            db.session.commit()
            print(httpslogin)
        # db.session.query(HTTPSLog).delete()
        # db.session.commit()
        return request.json
    else:
        resps = HTTPSLog.query.all()
        print(resps)
        return jsonify([i.https_serialize for i in resps])
