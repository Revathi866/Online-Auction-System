import socket
import threading
import sys
import ssl

HOST = "172.19.194.251"
PORT = 5555

auction_started = False


def receive_messages(client):
    global auction_started

    while True:
        try:
            msg = client.recv(1024).decode()
            if not msg:
                break

            if msg.startswith("START_COUNTDOWN") and not auction_started:
                sec = msg.split()[1]
                sys.stdout.write(f"\rAuction starts in: {sec} sec   ")
                sys.stdout.flush()
                continue

            if "AUCTION STARTED" in msg:
                auction_started = True
                print("\n" + msg + "\nTime limit: 20 sec\n")
                continue

            if not msg.startswith("TIMER"):
                print("\n" + msg)

        except:
            break


def start_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations("cert.pem")

    client = context.wrap_socket(sock, server_hostname=HOST)

    try:
        client.connect((HOST, PORT))
        print("Secure connection established")
    except Exception as e:
        print("Connection failed:", e)
        return

    print(client.recv(1024).decode())

    name = input().strip()
    client.send(name.encode())

    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

    while True:
        try:
            cmd = input("> ").strip()
            if not cmd:
                continue

            client.send(cmd.encode())

            if cmd.lower() == "exit":
                break

        except:
            break

    client.close()


if __name__ == "__main__":
    start_client()