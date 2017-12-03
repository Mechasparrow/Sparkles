import websocket
import threading
import time
import json

import copy

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
mining = False
alt_block = None
blk_dict = {}

def load_blockchain():

    try:
        blockchain = BlockChain.load_blockchain('./blockchain/blockchain.json')
    except FileNotFoundError:
        blocks = []
        blocks.append(genesis_block)
        genesis_block = Block.load_from_file('./genesis_block/genesis_block.json')
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

def mine(NUM_ZEROS=4):

    global mining
    global alt_block
    global blk_dict

    mining = True


    blk_dict['nonce'] = int(blk_dict['nonce'])

    while True:

        block_header_string = header_string(blk_dict['index'], blk_dict['prev_hash'], blk_dict['data'], blk_dict['timestamp'], blk_dict['nonce'])
        block_hash = generate_hash(block_header_string)

        if (mining == False):
            try:
                alt_blk_data = json.loads(alt_block.data)
                alt_blk_transaction = Transaction.from_json(alt_blk_data[0])

                mine_blk_data = json.loads(blk_dict['data'])
                mine_blk_transaction = Transaction.from_json(mine_blk_data[0])

                if (alt_blk_transaction == mine_blk_transaction):
                    mining = False
                    alt_block = None

                    print ("ALT BLOCK")
                    print ("BLEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEP")
                    return None
                    break
                else:
                    print ("Not BLEEEEEEEEEEEEEEEEEEEEEEEEEEP")
                    mining = True
                    alt_block = None

            except json.decoder.JSONDecodeError:
                mining = True

        print (block_hash)

        if (str(block_hash[0:NUM_ZEROS]) == '0' * NUM_ZEROS):
            blk_dict['hash'] = block_hash
            break

        blk_dict['nonce'] = blk_dict['nonce'] + 1

    return blk_dict

def blockchain_upload_message():

    global blockchain

    blockchain_message = {
        'message_type': 'blockchain_upload',
        'blockchain': str(blockchain)
    }

    blockchain_message_json = json.dumps(blockchain_message)

    return blockchain_message_json

def on_message(ws, message):
    message_decoded = json.loads(message)

    global blockchain

    global mining
    global alt_block
    global blk_dict

    if (message_decoded['message_type'] == 'transaction'):
        transaction_json = message_decoded['data']
        transaction = Transaction.from_json(transaction_json)
        if (transaction.validate_transaction() == True):
            block = create_block(transaction)
            print ("done mining. Sending block...")
            if not (block == None):
                block_message_json = block_message(block)
                ws.send(block_message_json)
            else:
                print ("Sorry there someone mined it first :P")

    elif (message_decoded['message_type'] == "sync_request"):
        print ("blockchain requested")

        ws.send(blockchain_upload_message())

    elif (message_decoded['message_type'] == "blockchain_upload"):
        recieved_blockchain = BlockChain.from_json(message_decoded['blockchain'])

        new_blockchain = BlockChain.sync_blockchain(blockchain, recieved_blockchain)

        blockchain = new_blockchain

        blockchain.save_blockchain('./blockchain/blockchain.json')

        print ()

    elif (message_decoded['message_type'] == 'new_block'):
        print ("new block!")

        block_json = message_decoded['block']
        block = Block.from_json(block_json)

        if (block.valid_block() == True):

            if (mining == True):
                alt_block = block
                mining = False

            temp_blocks = copy.copy(blockchain.blocks)

            temp_blocks.append(block)
            temp_block_chain = BlockChain(temp_blocks)

            if (temp_block_chain.validate_chain() == True):
                print ("valid new blockchain")
                blockchain.blocks.append(block)

                blk_dict = fresh_blk_dict(blk_dict['data'])
            else:
                print("invalid chain. Not updated")
        else:
            print ("invalid block")

        blockchain.save_blockchain('./blockchain/blockchain.json')

def block_message(block):

    block_message = {
        'message_type': 'new_block',
        'block': str(block)
    }

    block_message_json = json.dumps(block_message)

    return block_message_json

def fresh_blk_dict(data):

    iteration = len(blockchain.blocks)

    prev_block = blockchain.blocks[iteration - 1]

    blk_dict = {}
    blk_dict['index'] = iteration
    blk_dict['timestamp'] = date.datetime.now()
    blk_dict['data'] = str(data)
    blk_dict['prev_hash'] = prev_block.hash
    blk_dict['hash'] = None
    blk_dict['nonce'] = 0

    return blk_dict

def create_block(transaction):
    print ("mining block...")

    global blk_dict

    miner_secret = get_miner_secret()
    miner_address = get_miner_address()

    ## TODO fix this iteration bug
    iteration = len(blockchain.blocks)

    reward = Reward(miner_address, transaction.amnt, block_iteration = iteration, private_key = miner_secret )

    data = json.dumps([str(transaction), str(reward)])

    blk_dict = fresh_blk_dict(data)

    mined_block_data = mine()

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
def sync_message():
    sync = {
        'message_type': 'sync',
    }

    message_json = json.dumps(sync)
    return message_json

def on_open(ws):
    print ("### open ###")

    open_message = {
        'message_type': 'connection',
        'connection': True
    }

    open_message_json = json.dumps(open_message)

    ws.send(open_message_json)
    ws.send(blockchain_upload_message())
    ws.send(sync_message())

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
