from honeypot import configuration

import socket
import ssl
import time


def start_https_honeypot(ip='0.0.0.0'):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ip, configuration.settings.https_port))
        server_socket.listen(100)
        wrapped_socket = ssl.wrap_socket(server_socket, configuration.settings.ssl_key, configuration.settings.ssl_cert, True)

        while True:
            try:
                conn, addr = wrapped_socket.accept()
                req = conn.recv(1024)
                conn.sendall(b'HTTP/1.0 200 OK\n\nHello World')
                conn.close()
                with open(configuration.settings.https_log, "a") as f:
                    print(time.time(), addr[0]+";"+str(req))
                    f.write(str(time.time()) + ";" + addr[0]+";"+str(req)+"\n")
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    configuration.init('dev')
    start_https_honeypot()
