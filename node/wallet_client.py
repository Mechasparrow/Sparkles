import websocket
import _thread
import time
import json

import sys

sys.path.append("../CryptoWork")
sys.path.append("../block")
sys.path.append("../blockchain_lib")

from transaction import Transaction
from blockchain import BlockChain
from block import Block

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

def on_message(ws, message):
    message_decoded = json.loads(message)

    if (message_decoded['message_type'] == "message"):
        print (message_decoded['message'])
    elif (message_decoded['message_type'] == "new_block"):
        print ("New Block Recieved!")

        block_json = message_decoded['block']
        block = Block.from_json(block_json)

        blockchain.blocks.append(block)

        print (blockchain)

        blockchain.save_blockchain('./blockchain/blockchain.json')

        print()

def on_error(ws, error):
    print (error)

def on_close(ws):
    print ("### closed ###")

def get_keys():
    sk = crypto_key_gen.generate_key()
    pk = crypto_key_gen.get_public_key(sk)

    return sk, pk

def create_transaction(sk, pk, amnt, address):

    pk_hex = base64.b16encode(pk.to_string()).decode('utf-8')
    transaction = Transaction(pk_hex, address, str(amnt), note = "", private_key = sk)

    return transaction

def disconnect_message():
    disconnect = {
        'message_type': 'connection',
        'connection': False
    }

    message_json = json.dumps(disconnect)
    return message_json

def connect_message():
    connect = {
        'message_type': 'connection',
        'connection': True
    }

    message_json = json.dumps(connect)
    return message_json


def on_open(ws):
    print ("### open ###")

    public_key = crypto_key_gen.from_public_pem('./keys/public.pem')
    private_key = crypto_key_gen.from_private_pem('./keys/secret.pem')

    ws.send(connect_message())

    def run (*args):
        while (True):
            mode = input("What would you like to do? (transaction, balance, exit, nodes): ")

            if (mode == "exit"):
                ws.send(disconnect_message())
                ws.close()
                break
            elif (mode == "transaction"):
                print ("beginning transaction...")

                sk, pk = private_key, public_key
                transaction = create_transaction(sk, pk, 10, "a6b5d3avh10")

                transaction_data = {
                    "message_type": "transaction",
                    "data": str(transaction)
                }

                transaction_data_json = json.dumps(transaction_data)

                ws.send(transaction_data_json)


            elif (mode == "nodes"):
                command_data = {
                    "message_type": "command",
                    "command": "get_nodes"
                }

                command_data_json = json.dumps(command_data)

                ws.send(command_data_json)

                time.sleep(1)
        print ("thread terminating")

    _thread.start_new_thread(run, ())

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:5000/wallet",
        on_message = on_message,
        on_error = on_error,
        on_close = on_close
    )

    blockchain = load_blockchain()
    print (blockchain)

    ws.on_open = on_open
    ws.run_forever()
