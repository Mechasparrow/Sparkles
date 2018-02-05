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

blockchain = BlockChain([])

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

def header_string(index, prev_hash, data, timestamp, nonce):
    return str(index) + str(prev_hash) + str(data) + str(timestamp) + str(nonce)
def generate_hash(header_string):

    sha = hashlib.sha256()
    sha.update(header_string.encode('utf-8'))
    return sha.hexdigest()

def mine(block_dict, NUM_ZEROS=4):
    mine_block_dict = dict.copy(block_dict)

    mine_block_dict['nonce'] = int(mine_block_dict['nonce'])

    while True:

        block_header_string = header_string(mine_block_dict['index'], mine_block_dict['prev_hash'], mine_block_dict['data'], mine_block_dict['timestamp'], mine_block_dict['nonce'])
        block_hash = generate_hash(block_header_string)

        print (block_hash)

        if (str(block_hash[0:NUM_ZEROS]) == '0' * NUM_ZEROS):
            mine_block_dict['hash'] = block_hash
            break

        mine_block_dict['nonce'] = mine_block_dict['nonce'] + 1

    return mine_block_dict


def create_block(block_return, transaction):
    print ("mining block...")

    iteration = len(blockchain.blocks)

    prev_block = blockchain.blocks[iteration - 1]

    miner_secret = get_miner_secret()
    miner_address = get_miner_address()

    reward = Reward(miner_address, transaction.amnt, block_iteration = iteration, private_key = miner_secret )

    data = json.dumps([str(transaction), str(reward)])

    block_data = {}
    block_data['index'] = iteration
    block_data['timestamp'] = date.datetime.now()
    block_data['data'] = str(data)
    block_data['prev_hash'] = prev_block.hash
    block_data['hash'] = None
    block_data['nonce'] = 0

    mined_block_data = mine(block_data)

    new_block = Block.from_dict(mined_block_data)

    print (new_block)

    block_return.append(new_block)
    return block_return

# Handle transactions
def transaction_handler(broadcast_message, payload):

    transaction_raw = payload['data']
    tx = Transaction.from_json(transaction_raw)

    blk_return = []

    create_block(blk_return, tx)

    print (blk_return)

def upload_block(block, broadcast_message):

    block_upload_json = {
        "message_type": "block_upload",
        "data": str(block)
    }

    block_upload_message = json.dumps(block_upload_json)

    broadcast_message(block_upload_message)

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

client_thread = Client_P2P(PEER_LIST, server_thread, client_loop)

server_thread.start()
client_thread.start()

client_thread.join()
server_thread.exit()
