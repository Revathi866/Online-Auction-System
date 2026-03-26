# Online Auction System

## Overview

This project implements a real-time online auction system using TCP sockets with SSL/TLS security. It supports multiple clients, concurrent bidding, and ensures fairness using synchronized state management.

---

## Features

* TCP socket-based communication
* SSL/TLS secure data transfer
* Multi-client support using threading
* Real-time bidding with countdown timer
* Fair bidding with lock-based synchronization

---

## Technologies Used

* Python
* Socket Programming
* SSL/TLS
* Threading

---

## How to Run

### Start Server

```
python server.py
```

### Start Client

```
python temp_client.py
```

---

## Working

The client connects to the server using TCP. SSL/TLS is used to establish a secure connection. Clients place bids in real time, and the server manages the auction using timers and synchronization to ensure fairness.

---

## Note
* Both devices must be on the same network

---

