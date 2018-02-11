import websocket
import threading
import time
import json
import random

import sys
import copy

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

blockchain = BlockChain([]) # Create an empty blockchain

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

def load_blockchain(): ## Function for loading the blockchain from local copy
    try:
        blockchain = BlockChain.load_blockchain('./blockchain/blockchain.json')
        if (blockchain.validate_chain()):
            print ("BlockChain is valid")
    except FileNotFoundError:
        blocks = []
        genesis_block = Block.load_from_file('./genesis_block/genesis_block.json')
        blocks.append(genesis_block)
        blockchain = BlockChain(blocks)

    return blockchain

## When the client recieves a new block

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
            else:
                print("invalid chain. Not updated")
        else:
            print ("invalid block")
    except json.decoder.JSONDecodeError:
        print ("invalid block")

    blockchain.save_blockchain('./blockchain/blockchain.json')

    print ()

    sys.stdout.write(prompt_string())
    sys.stdout.flush()


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

    print (prompt_string())


def get_address_hex(public_key):
    pk_hex = base64.b16encode(public_key.to_string()).decode('utf-8')
    return pk_hex

def get_address(public_key):
    pk_hex = get_address_hex(public_key)
    print ("Your address below")
    print (pk_hex.lower())

def get_balance(pk_hex):

    balance = 0.0

    # TODO implement balance loading

    for block in blockchain.blocks:
        try:
            blk_data = json.loads(block.data)

            blk_transaction = Transaction.from_json(blk_data[0])
            blk_reward = Reward.from_json(blk_data[1])

            if (blk_transaction.sender_pub_key == pk_hex):
                balance = balance - float(blk_transaction.amnt)
                balance = balance - float(blk_reward.reward_amnt)

            if (blk_transaction.address == pk_hex):
                balance = balance + float(blk_transaction.amnt)

            if (blk_reward.recipient == pk_hex):
                balance = balance + blk_reward.block_reward

        except json.decoder.JSONDecodeError:
            continue

    return balance


def create_transaction(sk, pk, amnt, address):
    pk_hex = base64.b16encode(pk.to_string()).decode('utf-8')
    transaction = Transaction(pk_hex, address, str(amnt), note = "", private_key = sk)

    return transaction

def client_loop(send_message):

    print ("Welcome to Sparkles 2.0")

    upload_blockchain(send_message, [])
    request_blockchain(send_message)

    while True:

        response = input(prompt_string())

        if (response == "exit"):
            print ("Exiting")
            break
        elif (response == "address"):
            get_address(public_key)
        elif (response == "balance"):
            sk, pk = private_key, public_key

            pk_hex = get_address_hex(pk)
            balance = get_balance(pk_hex)

            print (balance)

        elif (response == "transaction"):

            print ("beginning transaction...")

            sk, pk = private_key, public_key ## Alias

            address = input("What address do you want to send to?: ")
            amnt = float(input("How much would you like to send?: "))

            pk_hex = get_address_hex(pk)

            ## TODO implement balance checking
            balance = get_balance(pk_hex)

            commission = amnt * 0.01
            total_amnt = amnt + commission

            print ("total amnt being sent is " + str(total_amnt))

            if ((balance - total_amnt) < 0):
                print ("can't send payment. Insufficient funds")
            else:
                transaction = create_transaction(sk, pk, amnt, address.upper())

                transaction_data = {
                    "message_type": "transaction",
                    "data": str(transaction)
                }

                transaction_data_json = json.dumps(transaction_data)

                send_message(transaction_data_json)


# Spin up the threads
server_thread = Server_P2P(PEER_LIST, SERVER_IP, SERVER_PORT)

# Add Handlers for the server side
server_thread.add_handler("blockchain_request", upload_blockchain)
server_thread.add_handler("blockchain_upload", sync_blockchain)
server_thread.add_handler("block_upload", block_recieve)

client_thread = Client_P2P(PEER_LIST, server_thread, client_loop)

# Load up a local copy of the blockchain
blockchain = load_blockchain()
print (blockchain)

server_thread.start()
client_thread.start()

client_thread.join()
server_thread.exit()
