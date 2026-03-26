import threading
import time


class AuctionManager:
    def __init__(self):
        self.lock = threading.Lock()

        self.items = [
            {"name": "Item 1", "base_price": 200},
            {"name": "Item 2", "base_price": 200},
            {"name": "Item 3", "base_price": 200},
            {"name": "Item 4", "base_price": 200},
            {"name": "Item 5", "base_price": 200}
        ]

        self.current_index = 0
        self.current_price = 200
        self.highest_bidder = None

        self.time_limit = 20
        self.remaining_time = 20

        self.auction_running = False
        self.history = []
        self.balances = {}

    def register_client(self, user):
        with self.lock:
            if user not in self.balances:
                self.balances[user] = 1000

    def welcome_message(self, user):
        return f"""
Welcome {user}!

Auction Rules:
1) Initial Balance: 1000
2) Base price: 200
3) Bid must be multiple of 10
4) Timer resets to 20 sec on every bid
5) If no bid in 20 sec → item sold
6) Command: bid <amount>
"""

    def get_current_item(self):
        item = self.items[self.current_index]
        return (
            f"\nCURRENT ITEM: {item['name']}\n"
            f"Base price: 200\n"
            f"Current price: {self.current_price}\n"
            f"Highest bidder: {self.highest_bidder}"
        )

    def place_bid(self, user, price):
        with self.lock:
            if not self.auction_running:
                return "Auction not started yet"

            if price % 10 != 0:
                return "Bid must be multiple of 10"

            if price <= self.current_price:
                return f"Bid must be higher than {self.current_price}"

            if self.balances[user] < price:
                return "Insufficient balance"

            if self.highest_bidder:
                self.balances[self.highest_bidder] += self.current_price

            self.balances[user] -= price
            self.current_price = price
            self.highest_bidder = user
            self.remaining_time = self.time_limit

            ts = time.strftime("%H:%M:%S")
            msg = (
                f"\nNEW BID\n{user} bid {price}\n"
                f"Balance: {self.balances[user]}\n"
                f"Current leader: {self.highest_bidder}"
            )

            self.history.append(f"[{ts}] {user} bid {price}")
            print(msg)
            return msg

    def decrease_timer(self):
        with self.lock:
            if self.remaining_time > 0:
                self.remaining_time -= 1

    def get_time(self):
        return self.remaining_time

    def start_auction(self):
        with self.lock:
            self.auction_running = True
            self.current_price = 200
            self.highest_bidder = None
            self.remaining_time = self.time_limit

    def close_current_item(self):
        winner = self.highest_bidder or "No bids"
        msg = (
            f"\nITEM SOLD\nWinner: {winner}\n"
            f"Final price: {self.current_price}\n"
        )
        print(msg)
        return msg

    def move_to_next_item(self):
        self.current_index += 1

        if self.current_index >= len(self.items):
            self.auction_running = False
            return "\n==== AUCTION FINISHED ====\n"

        self.current_price = 200
        self.highest_bidder = None
        self.remaining_time = self.time_limit

        item = self.items[self.current_index]
        return f"\n==== NEW ITEM ====\nNEXT ITEM: {item['name']}\nBase price: 200\n"

    def get_history(self):
        return "\n".join(self.history) if self.history else "No bids yet"