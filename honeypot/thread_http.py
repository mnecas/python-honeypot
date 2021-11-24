from honeypot import configuration
import socket


def start_http_honeypot(ip='0.0.0.0'):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ip, configuration.settings.http_port))
        server_socket.listen(100)
        while True:
            try:
                conn, addr = server_socket.accept()
                req = conn.recv(1024)
                conn.sendall(b"HTTP/1.0 200 OK\n\nHello World")
                conn.close()
                with open(configuration.settings.http_log, "a") as f:
                    print(addr[0]+";"+str(req))
                    f.write(addr[0]+";"+str(req)+"\n")
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    configuration.init('dev')
    start_http_honeypot()
