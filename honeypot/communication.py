from honeypot import configuration
import requests
import argparse
import json
import os



def get_args():
    parser = argparse.ArgumentParser(description='Python honeypot communication')
    parser.add_argument('--server-ip')
    parser.add_argument('--prod', action='store_true')
    return parser.parse_args()


def get_ssh_log():
    if os.path.exists(configuration.settings.ssh_log):
        resp = []
        with open(configuration.settings.ssh_log, 'r') as f:
            print(configuration.settings.ssh_log)
            for i in f.readlines():
                sp = i.split(';')
                resp.append({
                    'ip':sp[0],
                    'username':sp[1],
                    'password':';'.join(sp[2:]).rstrip(),
                })
        # Cleanup data from file
        # open(configuration.settings.ssh_log, 'w').close()
        return json.dumps(resp)


if __name__ == "__main__":
    args = get_args()
    print("Starting the server.")
    threads = []
    if args.prod:
        print("Server started in production mode.")
        configuration.init('prod')
    else:
        print("Server started in dev mode.")
        configuration.init('dev')
    url = f"{args.server_ip}/api/ssh"
    data = get_ssh_log()
    headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
    print(data)
    x = requests.post(url, data=json.dumps(headers), headers=headers)
    print("resp", x.text)
