import socket
import threading
import ssl

from auction_client import handle_client
from models import start_timer
from logic import AuctionManager

HOST = "172.19.194.251"
PORT = 5555

clients = []
lock = threading.Lock()
auction = AuctionManager()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(10)

    print("Auction Server Started (SSL Enabled)")
    print("Waiting for clients...")

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain("cert.pem", "key.pem")

    start_timer(auction, clients, lock)

    try:
        while True:
            conn, addr = server.accept()
            secure_conn = context.wrap_socket(conn, server_side=True)

            print("Connected from:", addr)

            secure_conn.send(b"Enter your name: ")
            name = secure_conn.recv(1024).decode().strip()

            threading.Thread(
                target=handle_client,
                args=(secure_conn, addr, name, clients, lock, auction),
                daemon=True
            ).start()

    except KeyboardInterrupt:
        print("\nServer shutting down...")

    finally:
        server.close()


if __name__ == "__main__":
    start_server()