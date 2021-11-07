from honeypot import configuration

import socket
import threading
import paramiko

LOGFILE_LOCK = threading.Lock()


class SSHServer(paramiko.ServerInterface):
    def __init__(self, addr):
        self.event = threading.Event()
        self.addr = addr

    def check_auth_password(self, username, password):
        LOGFILE_LOCK.acquire()
        try:
            with open(configuration.settings.ssh_log, "a") as f:
                print("Login: " + self.addr[0] + ";" + username + ";" + password)
                f.write(self.addr[0]+";"+username + ";" + password + "\n")
        finally:
            LOGFILE_LOCK.release()
        return paramiko.AUTH_FAILED


def handle_ssh_connection(client, addr):
    transport = paramiko.Transport(client)
    host_key = paramiko.RSAKey(filename=configuration.settings.ssh_key)
    transport.add_server_key(host_key)
    server = SSHServer(addr)
    try:
        transport.start_server(server=server)
        channel = transport.accept(1)
        if channel is not None:
            channel.close()
    except ConnectionResetError:
        print('Closed ssh connection from: ' + addr[0])


def start_ssh_honeypot(ip='0.0.0.0'):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ip, configuration.settings.ssh_port))
        server_socket.listen(100)
        paramiko.util.log_to_file(configuration.settings.paramiko_log)

        while True:
            try:
                conn, addr = server_socket.accept()
                t = threading.Thread(target=handle_ssh_connection, args=(conn, addr, ))
                t.deamon = True
                t.start()
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    configuration.init('dev')
    start_ssh_honeypot()
