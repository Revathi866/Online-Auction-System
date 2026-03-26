import threading
import time


def broadcast(msg, clients, lock):
    with lock:
        for c in clients[:]:
            try:
                c.send((msg + "\n").encode())
            except:
                if c in clients:
                    clients.remove(c)


def timer_loop(auction, clients, lock):
    print("\nServer started.\nPreparing auction...\n")

    # 🔹 Countdown (20 sec)
    for r in range(50, 0, -1):
        print(f"\rAuction starts in: {r} sec", end="", flush=True)
        broadcast(f"START_COUNTDOWN {r}", clients, lock)
        time.sleep(1)

    print()

    # 🔥 START AUCTION FIX
    auction.start_auction()

    msg = "\n==== AUCTION STARTED ====\n"
    print(msg)
    broadcast(msg, clients, lock)

    # 🔥 Ensure Item 1 shows
    first_item = auction.get_current_item()
    print(first_item)
    broadcast(first_item, clients, lock)

    time.sleep(0.2)

    broadcast(f"TIMER {auction.get_time()}", clients, lock)

    # 🔹 Main loop
    while True:
        time.sleep(1)

        if not auction.auction_running:
            continue

        with auction.lock:
            if auction.remaining_time > 0:
                auction.remaining_time -= 1
            t = auction.remaining_time

        print(f"\rTime remaining: {t} sec", end="", flush=True)
        broadcast(f"TIMER {t}", clients, lock)

        if t == 0:
            print()

            broadcast(auction.close_current_item(), clients, lock)

            nxt = auction.move_to_next_item()
            print(nxt)
            broadcast(nxt, clients, lock)

            time.sleep(0.2)
            broadcast(f"TIMER {auction.get_time()}", clients, lock)


def start_timer(auction, clients, lock):
    threading.Thread(
        target=timer_loop,
        args=(auction, clients, lock),
        daemon=True
    ).start()

    print("Timer thread started.")