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

from transaction import Transaction
from block import Block

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
            create_block(transaction)

def create_block(transaction):
    print ("mining block...")

    data = [str(transaction)]

    block_data = {}
    block_data['index'] = 1
    block_data['timestamp'] = date.datetime.now()
    block_data['data'] = str(data)
    block_data['prev_hash'] = None
    block_data['hash'] = None
    block_data['nonce'] = 0

    mined_block_data = mine(block_data)

    new_block = Block.from_dict(mined_block_data)
    print (new_block)

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

    ws.on_open = on_open
    ws.run_forever()
