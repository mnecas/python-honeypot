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
            with open('/var/log/python-honeypot/ssh_logins.log', "a") as f:
                print("Login: " + self.addr[0] + ";" + username + ";" + password)
                f.write(self.addr[0]+";"+username + ";" + password + "\n")
        finally:
            LOGFILE_LOCK.release()
        return paramiko.AUTH_FAILED


def handle_ssh_connection(client, addr, ssh_key):
    transport = paramiko.Transport(client)
    host_key = paramiko.RSAKey(filename=ssh_key)
    transport.add_server_key(host_key)
    server = SSHServer(addr)
    try:
        transport.start_server(server=server)
        channel = transport.accept(1)
        if channel is not None:
            channel.close()
    except ConnectionResetError:
        print('Closed ssh connection from: ' + addr[0])


def start_ssh_honeypot(ip='0.0.0.0', port=22, ssh_key='~/.ssh/honeypot.key'):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ip, port))
        server_socket.listen(100)
        paramiko.util.log_to_file('/var/log/python-honeypot/paramiko.log')

        while True:
            try:
                conn, addr = server_socket.accept()
                t = threading.Thread(target=handle_ssh_connection, args=(conn, addr, ssh_key, ))
                t.start()
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    start_ssh_honeypot(port=8022)
