import socket
import ssl


def start_https_honeypot(ip='0.0.0.0', port=443):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ip, port))
        server_socket.listen(100)
        wrapped_socket = ssl.wrap_socket(server_socket, "keys/key.pem", "keys/cert.pem", True)

        while True:
            try:
                conn, addr = wrapped_socket.accept()
                req = conn.recv(1024)
                print(req)
                conn.close()
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    start_https_honeypot(port=8043)
