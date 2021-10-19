import honeypot.http
import honeypot.ssh
import argparse
import threading
import signal

def get_args():
    parser = argparse.ArgumentParser(description='Python honeypot')
    parser.add_argument('--prod', action='store_true')
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    print("Starting the server.")
    threads = []
    if args.prod:
        print("Server started in production mode.")
        threads.append(threading.Thread(target=honeypot.ssh.start_ssh_honeypot))
        threads.append(threading.Thread(target=honeypot.http.start_http_honeypot))
    else:
        print("Server started in dev mode.")
        # Create thread list with all honepot services
        threads.append(threading.Thread(target=honeypot.ssh.start_ssh_honeypot, kwargs={'port':8022}))
        threads.append(threading.Thread(target=honeypot.http.start_http_honeypot, kwargs={'port':8080}))

    # Start threads
    for thread in threads:
        thread.start()
