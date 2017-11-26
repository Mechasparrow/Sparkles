import websocket
import _thread
import time
import json

import hashlib
import datetime as date

import sys

sys.path.append("../CryptoWork")
sys.path.append("../block")
sys.path.append("../node")
sys.path.append("../blockchain_lib")

from transaction import Transaction
from blockchain import BlockChain
from block import Block
from reward import Reward
import crypto_key_gen
import base64

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

def get_miner_address(sk):

    pk = crypto_key_gen.get_public_key(sk)
    pk_hex = base64.b16encode(pk.to_string()).decode('utf-8')

    return pk_hex

def get_miner_secret():
    sk = crypto_key_gen.generate_key()
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



def on_message(ws, message):
    message_decoded = json.loads(message)
    if (message_decoded['message_type'] == 'transaction'):
        transaction_json = message_decoded['data']
        transaction = Transaction.from_json(transaction_json)
        if (transaction.validate_transaction() == True):
            block = create_block(transaction)
            print ("done mining. Sending block...")
            block_message_json = block_message(block)
            ws.send(block_message_json)
    elif (message_decoded['message_type'] == 'new_block'):
        print ("new block!")

        block_json = message_decoded['block']
        block = Block.from_json(block_json)

        blockchain.blocks.append(block)

        print (blockchain)

        blockchain.save_blockchain('./blockchain/blockchain.json')

def block_message(block):

    block_message = {
        'message_type': 'new_block',
        'block': str(block)
    }

    block_message_json = json.dumps(block_message)

    return block_message_json

def create_block(transaction):
    print ("mining block...")


    iteration = len(blockchain.blocks)

    prev_block = blockchain.blocks[iteration - 1]

    miner_secret = get_miner_secret()
    miner_address = get_miner_address(miner_secret)

    reward = Reward(miner_address, 10, block_iteration = iteration, private_key = miner_secret )

    data = [str(transaction), str(reward)]

    block_data = {}
    block_data['index'] = iteration
    block_data['timestamp'] = date.datetime.now()
    block_data['data'] = str(data)
    block_data['prev_hash'] = prev_block.hash
    block_data['hash'] = None
    block_data['nonce'] = 0

    mined_block_data = mine(block_data)

    new_block = Block.from_dict(mined_block_data)
    return new_block

def on_error(ws, error):
    print (error)

def on_close(ws):

    close_message = {
        'message_type': 'connection',
        'connection': False
    }

    close_message_json = json.dumps(close_message)
    ws.send(close_message_json)

    print ("### closed ###")

def on_open(ws):
    print ("### open ###")

    open_message = {
        'message_type': 'connection',
        'connection': True
    }

    open_message_json = json.dumps(open_message)

    ws.send(open_message_json)


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:5000/miners",
        on_message = on_message,
        on_error = on_error,
        on_close = on_close
    )

    blockchain = load_blockchain()
    print (blockchain)

    ws.on_open = on_open
    ws.run_forever()
