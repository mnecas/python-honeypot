from honeypot.ssh import start_ssh_honeypot 
import argparse

def get_args():
    parser = argparse.ArgumentParser(description='Python honeypot')
    parser.add_argument('--dev', action='store_true')
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    if args.dev:
        start_ssh_honeypot(ssh_port=10022)
    else:
        start_ssh_honeypot()