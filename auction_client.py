def broadcast(msg, clients, lock):
    with lock:
        for c in clients[:]:
            try:
                c.send((msg + "\n").encode())
            except:
                if c in clients:
                    clients.remove(c)


def handle_client(conn, addr, name, clients, lock, auction):
    print(f"{name} connected from {addr}")

    auction.register_client(name)

    with lock:
        clients.append(conn)

    conn.send(auction.welcome_message(name).encode())

    try:
        while True:
            conn.send(b"\nCommands:\nbid <amount>\nhistory\nexit\n")

            try:
                data = conn.recv(1024)
                if not data:
                    break
                data = data.decode().strip()

            except ConnectionResetError:
                print(f"{name} disconnected unexpectedly")
                break

            cmd = data.split()
            if not cmd:
                continue

            if cmd[0] == "bid":
                if len(cmd) != 2:
                    conn.send(b"Usage: bid <amount>\n")
                    continue

                try:
                    price = int(cmd[1])
                except:
                    conn.send(b"Invalid amount\n")
                    continue

                result = auction.place_bid(name, price)
                broadcast(result, clients, lock)

            elif cmd[0] == "history":
                conn.send(auction.get_history().encode())

            elif cmd[0] == "exit":
                break

            else:
                conn.send(b"Invalid command\n")

    finally:
        with lock:
            if conn in clients:
                clients.remove(conn)

        conn.close()
        broadcast(f"{name} left the auction", clients, lock)
        print(f"{name} disconnected")