import websocket
import threading
from threading import Thread

import time
import json
import random

import copy

import hashlib
import datetime as date

import sys

sys.path.append("../CryptoWork")
sys.path.append("../block")
sys.path.append("../node")
sys.path.append("../blockchain_lib")
sys.path.append("../p2p-networking")

from transaction import Transaction
from blockchain import BlockChain
from block import Block
from reward import Reward
import crypto_key_gen
import base64

from peerhttp import PeerHTTP

import peer_search

# Import p2p server
from server_p2p_node import Server_P2P

# Import p2p client
from client_p2p_node import Client_P2P

# Import broadcast protocol
from peer_broadcast import PeerBroadcast

## Setup

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

# Client and Server Handlers

# Public and Private key for transactions
public_key = crypto_key_gen.from_public_pem('./keys/public.pem')
private_key = crypto_key_gen.from_private_pem('./keys/secret.pem')

def client_loop(send_message):

    print ("Welcome to Sparkles 2.0 (Miner)")

    pass

# Spin up the threads
server_thread = Server_P2P(PEER_LIST, SERVER_IP, SERVER_PORT)

client_thread = Client_P2P(PEER_LIST, server_thread, client_loop)

server_thread.start()
client_thread.start()

client_thread.join()
server_thread.exit()
