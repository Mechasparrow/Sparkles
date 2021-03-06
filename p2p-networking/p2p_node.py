import socket
import time
import threading
import random

import json
import copy
import sys

from peerhttp import PeerHTTP

import peer_search

# Import p2p server
from server_p2p_node import Server_P2P

# Import p2p client
from client_p2p_node import Client_P2P

# Import broadcast protocol
from peer_broadcast import PeerBroadcast


## Find peers
EXTERNAL_IP = PeerHTTP.get_external_ip()

## TODO do on LAN

start_port = 3000

PEER_LIST = peer_search.local_search(EXTERNAL_IP)

## Server code

SERVER_IP = PeerHTTP.get_local_ip()
SERVER_PORT = random.randint(start_port, start_port + 3000)

post_peer = PeerHTTP.post_local_peer(EXTERNAL_IP, SERVER_IP, SERVER_PORT)

if (post_peer):
    print ("Server posted")
else:
    print ("Server not posted")

# Client code

def client_loop(send_message):

    while True:

        # Broadcast messages

        message = input ("what would you like to broadcast? (exit): ")

        if (message == "exit"):
            print ("exiting")
            break
        else:
            send_message(message)

# Server Code

def cat_handler(broadcast_message, payload):
    print (payload)
    broadcast_message("Meowz")

server_thread = Server_P2P(PEER_LIST, SERVER_IP, SERVER_PORT)

server_thread.add_handler("cats", cat_handler)

client_thread = Client_P2P(PEER_LIST, server_thread, client_loop)

server_thread.start()
client_thread.start()

client_thread.join()
server_thread.exit()
