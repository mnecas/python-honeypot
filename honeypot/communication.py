from honeypot import configuration
import requests
import argparse
import json
import os


def get_args():
    # Argparse to get the server ip on which the json
    # request will be sent.
    parser = argparse.ArgumentParser(
        description='Python honeypot communication')

    # Example `--server-ip localhost:5000`
    # Which specifies the hostname and the port
    # on which the request will be sent.
    parser.add_argument('--server-ip')

    # The prod mode tell us for which logfiles the data
    # should be sent to the server.
    parser.add_argument('--prod', action='store_true')
    return parser.parse_args()


def get_http_log():
    if os.path.exists(configuration.settings.http_log):
        # The list of data which will be sent to the server.
        resp = []
        # Reading the logfile from file, the file path depends on the dev or prod mode
        with open(configuration.settings.http_log, 'r') as f:
            # Some logs for user
            print(configuration.settings.http_log)
            for i in f.readlines():
                sp = i.split(';')
                # Sending the user data.
                resp.append({
                    'time': sp[0],
                    'ip': sp[1]
                })
        # Cleanup data from file.
        open(configuration.settings.http_log, 'w').close()
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
        # Cleanup data from file.
        open(configuration.settings.http_log, 'w').close()
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
        open(configuration.settings.ssh_log, 'w').close()
        return json.dumps(resp)


if __name__ == "__main__":
    args = get_args()
    # Inicilize the setting depending on the argparser prod/dev.
    if args.prod:
        configuration.init('prod')
    else:
        configuration.init('dev')
    # Dict of the services which the honeypot support.
    # The key is the name of the service and the value.
    # is the functions which return the data which will
    # be sent to the honeypot web.
    send_list = {
        'ssh': get_ssh_log,
        'http': get_http_log,
        'https': get_https_log,
    }
    # Headers with which the request will be sent so the
    # web server will know that we are sending json data.
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json'}
    # We go through all key/values in send_list and use the key
    # as API endpoint and we get the data form the value function
    for key, get_data_fce in send_list.items():
        url = f"http://{args.server_ip}/api/{key}"
        print("URL:", url)
        data = get_data_fce()
        if data:
            x = requests.post(url, data=json.dumps(data), headers=headers)
            print("Resp:", x.text)
