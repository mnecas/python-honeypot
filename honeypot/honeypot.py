import configuration
import thread_http, thread_https, thread_ssh
import argparse
import threading


def get_args():
    parser = argparse.ArgumentParser(description='Python honeypot')
    parser.add_argument('--prod', action='store_true')
    return parser.parse_args()


if __name__ == "__main__":
    # There is configuration file with init which will set the config setting 
    # depending on which version of the program is running
    # The production is runing on proper linux directories like.
    # /var/log where are stored logs
    # /etc/pki/tls where are stored ssl keys
    # ~/.ssh where are stored ssh keys
    # If it runs in the dev mode it runs in the keys or logs direcotry.
    # Also affects the port numbers of the honeypots
    # SSH prod=22 dev=8022
    # HTTP prod=80 dev=8080
    # HTTPS prod=443 dev=8043
    args = get_args()
    print("Starting the server.")
    # List of thread which will the honeypot start
    threads = []
    if args.prod:
        print("Server started in production mode.")
        configuration.init('prod')
    else:
        print("Server started in dev mode.")
        configuration.init('dev')
    # Create thread list with all honepot services
    threads.append(threading.Thread(target=thread_ssh.start_ssh_honeypot))
    threads.append(threading.Thread(target=thread_http.start_http_honeypot))

    threads.append(threading.Thread(target=thread_https.start_https_honeypot))
    # Start threads
    for thread in threads:
        thread.start()
