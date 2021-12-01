from honeypot import configuration
import requests
import argparse
import json
import os


def get_args():
    parser = argparse.ArgumentParser(
        description='Python honeypot communication')
    parser.add_argument('--server-ip')
    parser.add_argument('--prod', action='store_true')
    return parser.parse_args()


def get_http_log():
    if os.path.exists(configuration.settings.http_log):
        resp = []
        with open(configuration.settings.http_log, 'r') as f:
            print(configuration.settings.http_log)
            for i in f.readlines():
                sp = i.split(';')
                resp.append({
                    'time': sp[0],
                    'ip': sp[1]
                })
        # Cleanup data from file
        # open(configuration.settings.http_log, 'w').close()
        return json.dumps(resp)


def get_https_log():
    if os.path.exists(configuration.settings.https_log):
        resp = []
        with open(configuration.settings.https_log, 'r') as f:
            print(configuration.settings.https_log)
            for i in f.readlines():
                sp = i.split(';')
                resp.append({
                    'time': sp[0],
                    'ip': sp[1]
                })
        # Cleanup data from file
        # open(configuration.settings.http_log, 'w').close()
        return json.dumps(resp)


def get_ssh_log():
    if os.path.exists(configuration.settings.ssh_log):
        resp = []
        with open(configuration.settings.ssh_log, 'r') as f:
            print(configuration.settings.ssh_log)
            for i in f.readlines():
                sp = i.split(';')
                resp.append({
                    'time': sp[0],
                    'ip': sp[1],
                    'username': sp[2],
                    'password': ';'.join(sp[3:]).rstrip(),
                })
        # Cleanup data from file
        # open(configuration.settings.ssh_log, 'w').close()
        return json.dumps(resp)


if __name__ == "__main__":
    args = get_args()
    threads = []
    if args.prod:
        configuration.init('prod')
    else:
        configuration.init('dev')
    send_list = {
        'ssh': get_ssh_log,
        'http': get_http_log,
        'https': get_https_log,
    }
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json'}
    for key, send_fce in send_list.items():
        url = f"http://{args.server_ip}/api/{key}"
        print("URL:", url)
        data = send_fce()
        if data:
            x = requests.post(url, data=json.dumps(data), headers=headers)
            print("Resp:", x.text)
