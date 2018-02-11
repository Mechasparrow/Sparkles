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

from miner import BlockMiner

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

blockchain = BlockChain([])

miners = []

def load_blockchain():

    try:
        blockchain = BlockChain.load_blockchain('./blockchain/blockchain.json')
    except FileNotFoundError:
        blocks = []
        genesis_block = Block.load_from_file('./genesis_block/genesis_block.json')
        blocks.append(genesis_block)
        blockchain = BlockChain(blocks)

    return blockchain

def get_miner_address():

    pk = crypto_key_gen.from_public_pem('./keys/public.pem')
    pk_hex = base64.b16encode(pk.to_string()).decode('utf-8')

    return pk_hex

def get_miner_secret():
    sk = crypto_key_gen.from_private_pem('./keys/secret.pem')
    return sk

# Handle transactions
def transaction_handler(broadcast_message, payload):

    transaction_raw = payload['data']
    tx = Transaction.from_json(transaction_raw)

    if (tx.validate_transaction()):

        block_miner = BlockMiner(tx, blockchain, get_miner_address(), get_miner_secret())

        block_miner.start()
        miners.append(block_miner)

        new_block = block_miner.join()

        miners.remove(block_miner)

        if (new_block == None):
            print ("Someone beat you to it")
            return

        good_block = update_blockchain(new_block)

        if (good_block == True):
            upload_block(new_block, broadcast_message)
        else:
            print ("That was a pretty bad block, so were not going to send it out to peers")

def update_blockchain(block):

    if (block.valid_block() == True):

        temp_blocks = copy.copy(blockchain.blocks)

        temp_blocks.append(block)
        temp_block_chain = BlockChain(temp_blocks)

        if (temp_block_chain.validate_chain() == True):
            print ("valid new blockchain")
            blockchain.blocks.append(block)
            return True
        else:
            print("invalid chain. Not updated")
            return False
    else:
        print ("invalid block")
        return False

    blockchain.save_blockchain('./blockchain/blockchain.json')

def upload_block(block, broadcast_message):

    block_upload_json = {
        "message_type": "block_upload",
        "data": str(block)
    }

    block_upload_message = json.dumps(block_upload_json)

    broadcast_message(block_upload_message)

def block_recieve(broadcast_message, payload):

    print()
    print ("NEW BLOCK RECIEVED")

    block_json = payload['data']

    try:
        block = Block.from_json(block_json)

        if (block.valid_block() == True):
            temp_blocks = copy.copy(blockchain.blocks)

            temp_blocks.append(block)
            temp_block_chain = BlockChain(temp_blocks)

            print (temp_block_chain)

            if (temp_block_chain.validate_chain() == True):
                print ("valid new blockchain")
                blockchain.blocks.append(block)

                for miner in miners:
                    if (miner.is_active()):
                        miner.intercept_block(block, blockchain)

            else:
                print("invalid chain. Not updated")
        else:
            print ("invalid block")
    except json.decoder.JSONDecodeError:
        print ("invalid block")

    blockchain.save_blockchain('./blockchain/blockchain.json')

    print ()

## Request blockchains from peers
def request_blockchain(send_message):

    message_json = {
        "message_type": "blockchain_request"
    }

    request_message = json.dumps(message_json)

    send_message(request_message)

## Upload blockchain to peer
def upload_blockchain(broadcast_message, payload):

    print ("preparing to broadcast message");

    blockchain_json = {
        "message_type": "blockchain_upload",
        "data": str(blockchain)
    }

    blockchain_message = json.dumps(blockchain_json)

    broadcast_message(blockchain_message)

## Sync blockchain
def sync_blockchain(broadcast_message, payload):

    print ("preparing for sync")

    global blockchain

    recv_blockchain_raw = json.loads(payload["data"])

    recieved_blockchain = BlockChain.from_json(payload["data"])

    synced_blockchain = BlockChain.sync_blockchain(blockchain, recieved_blockchain)

    blockchain = synced_blockchain

    blockchain.save_blockchain('./blockchain/blockchain.json')

    print ("blockchain synced")

    print()

def client_loop(send_message):

    print ("Welcome to Sparkles 2.0 (Miner)")

    upload_blockchain(send_message, [])
    request_blockchain(send_message)


    while True:

        continue

# Spin up the threads
server_thread = Server_P2P(PEER_LIST, SERVER_IP, SERVER_PORT)

#Load blockchain
blockchain = load_blockchain()

# Add handlers

server_thread.add_handler("transaction", transaction_handler)

# For handling blockchain stuff
server_thread.add_handler("blockchain_request", upload_blockchain)
server_thread.add_handler("blockchain_upload", sync_blockchain)
server_thread.add_handler("block_upload", block_recieve)

client_thread = Client_P2P(PEER_LIST, server_thread, client_loop)

server_thread.start()
client_thread.start()

client_thread.join()
server_thread.exit()
