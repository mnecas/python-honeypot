import yaml
import os

HOST_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(
    ".")), 'honeypot', 'deploy', 'inventory', 'ansible-hosts')

def read_yaml_file():
    # Open yaml file data from the host file
    with open(HOST_FILE_PATH, 'r') as f:
        resp = yaml.load(f, Loader=yaml.FullLoader)
    return resp


def write_yaml_file(data):
    # Write yaml data to the file
    with open(HOST_FILE_PATH, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)


def add_host(host, port=22):
    # Add host to the ansible hosts
    # We also set default user to root and the port
    hosts = read_yaml_file()
    hosts['honeypots']['hosts'][host] = {"ansible_user":"root", "ansible_port": port}
    write_yaml_file(hosts)


def remove_host(host):
    # Remove ansible host from the yaml file
    hosts = read_yaml_file()
    del hosts['honeypots']['hosts'][host]
    write_yaml_file(hosts)


def remove_all_host():
    # Remove all ansible hosts form the yaml file
    hosts = read_yaml_file()
    for key in list(hosts['honeypots']['hosts']):
        del hosts['honeypots']['hosts'][key]
    write_yaml_file(hosts)
