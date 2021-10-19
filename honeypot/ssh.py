import socket
import sys
import threading
import _thread
import paramiko

LOGFILE_LOCK = threading.Lock()


class SSHServer(paramiko.ServerInterface):
    def __init__(self, addr):
        self.event = threading.Event()
        self.addr = addr

    def check_auth_password(self, username, password):
        LOGFILE_LOCK.acquire()
        try:
            with open('ssh_logins.log',"a") as f:
                print("Login: "+ self.addr[0] + ";" + username + ";" + password)
                f.write(self.addr[0]+";"+username + ";" + password + "\n")
        finally:
            LOGFILE_LOCK.release()
        return paramiko.AUTH_FAILED


def handle_ssh_connection(client, addr, ssh_key):
    transport = paramiko.Transport(client)
    host_key = paramiko.RSAKey(filename=ssh_key)
    transport.add_server_key(host_key)
    server = SSHServer(addr)
    transport.start_server(server=server)
    channel = transport.accept(1)
    if not channel is None:
        channel.close()


def start_ssh_honeypot(ip='0.0.0.0', ssh_port=22, ssh_key='ssh.key'):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ip, ssh_port))
        server_socket.listen(100)
        paramiko.util.log_to_file('paramiko.log') 

        while True:
            try:
                conn, addr = server_socket.accept()
                _thread.start_new_thread(handle_ssh_connection,(conn, addr, ssh_key, ))
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    start_ssh_honeypot()
