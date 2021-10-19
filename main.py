from honeypot.ssh import start_ssh_honeypot 
import argparse

def get_args():
    parser = argparse.ArgumentParser(description='Python honeypot')
    parser.add_argument('--dev', action='store_true')
    return parser.parse_args()

if __name__ == "__main__":
    print("Starting the server.")
    args = get_args()
    if args.dev:
        print("Server started in dev mode.")
        start_ssh_honeypot(ssh_port=10022)
    else:
        print("Server started in production mode.")
        start_ssh_honeypot()
