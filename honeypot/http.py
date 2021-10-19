import socket


def start_http_honeypot(ip='0.0.0.0', port=80):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ip, port))
        server_socket.listen(100)
        while True:
            try:
                conn, addr = server_socket.accept()
                req = conn.recv(1024)
                print(req)
                conn.close()
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    start_http_honeypot(port=8080)
