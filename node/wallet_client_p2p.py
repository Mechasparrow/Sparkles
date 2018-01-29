import websocket
import threading
import time
import json
import random

import sys

sys.path.append("../CryptoWork")
sys.path.append("../block")
sys.path.append("../blockchain_lib")
sys.path.append("../mine")
sys.path.append("../p2p-networking")

from transaction import Transaction
from reward import Reward
from blockchain import BlockChain
from block import Block

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

def prompt_string():
    return "What would you like to do? (transaction, address, balance, exit): "

def get_address_hex(public_key):
    pk_hex = base64.b16encode(public_key.to_string()).decode('utf-8')
    return pk_hex

def get_address(public_key):
    pk_hex = get_address_hex(public_key)
    print ("Your address below")
    print (pk_hex.lower())

def create_transaction(sk, pk, amnt, address):
    pk_hex = base64.b16encode(pk.to_string()).decode('utf-8')
    transaction = Transaction(pk_hex, address, str(amnt), note = "", private_key = sk)

    return transaction

def client_loop(send_message):

    print ("Welcome to Sparkles 2.0")

    while True:

        response = input(prompt_string())

        if (response == "exit"):
            print ("Exiting")
            break
        elif (response == "address"):
            get_address(public_key)
        elif (response == "transaction"):

            print ("beginning transaction...")

            sk, pk = private_key, public_key ## Alias

            address = input("What address do you want to send to?: ")
            amnt = float(input("How much would you like to send?: "))

            pk_hex = get_address_hex(pk)

            ## TODO implement balance checking

            transaction = create_transaction(sk, pk, amnt, address.upper())

            print (str(transaction))

# Spin up the threads
server_thread = Server_P2P(PEER_LIST, SERVER_IP, SERVER_PORT)

client_thread = Client_P2P(PEER_LIST, server_thread, client_loop)

server_thread.start()
client_thread.start()

client_thread.join()
server_thread.exit()
