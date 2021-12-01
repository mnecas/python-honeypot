from honeypot import configuration
import socket
import time


def start_http_honeypot(ip='0.0.0.0'):
    try:
        # We create socket listener which we bind on our default address
        # and set it on port which was set in the configuration.
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ip, configuration.settings.http_port))
        server_socket.listen(100)
        while True:
            try:
                # Listen until we get the request.
                conn, addr = server_socket.accept()
                # Recieve first 1KB of data
                req = conn.recv(1024)
                # We sent user some data so he could see it on his broswer or
                # curl request, so he would not suspisous why would we have
                # open http port wihtout any webserver.
                conn.sendall(b"HTTP/1.0 200 OK\n\nHello World")
                # Right after the request we close the connection.
                conn.close()
                with open(configuration.settings.http_log, "a") as f:
                    print(str(time.time()) + ";" + addr[0]+";"+str(req))
                    # Log to the proper file depending on the config.
                    f.write(str(time.time()) + ";" + addr[0]+";"+str(req)+"\n")
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    # If we run this file by itself we assume  that the developer is running it
    # so we set up dev config and start the service by itself.
    configuration.init('dev')
    start_http_honeypot()
