import websocket
import threading
import time
import json

import copy

import sys

sys.path.append("../CryptoWork")
sys.path.append("../block")
sys.path.append("../blockchain_lib")
sys.path.append("../mine")

from transaction import Transaction
from reward import Reward
from blockchain import BlockChain
from block import Block

import crypto_key_gen
import base64

blockchain = BlockChain([])

def load_blockchain():
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

def prompt_string():
    return "What would you like to do? (transaction, address, balance, exit, nodes): "

def on_message(ws, message):
    message_decoded = json.loads(message)

    if (message_decoded['message_type'] == "message"):
        print (message_decoded['message'])
    elif (message_decoded['message_type'] == "new_block"):
        print ()
        print ("New Block Recieved!")

        block_json = message_decoded['block']
        block = Block.from_json(block_json)

        if (block.valid_block() == True):
            temp_blocks = copy.copy(blockchain.blocks)

            temp_blocks.append(block)
            temp_block_chain = BlockChain(temp_blocks)

            if (temp_block_chain.validate_chain() == True):
                print ("valid new blockchain")
                blockchain.blocks.append(block)
            else:
                print("invalid chain. Not updated")
        else:
            print ("invalid block")

        blockchain.save_blockchain('./blockchain/blockchain.json')

        print ()

        sys.stdout.write(prompt_string())
        sys.stdout.flush()

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

def sync_message():
    sync = {
        'message_type': 'sync',
    }

    message_json = json.dumps(sync)
    return message_json

def on_open(ws):
    print ("### open ###")

    public_key = crypto_key_gen.from_public_pem('./keys/public.pem')
    private_key = crypto_key_gen.from_private_pem('./keys/secret.pem')

    ws.send(connect_message())
    ws.send(sync_message())

    ended = False

    def run ():
        while (True):

            mode = input(prompt_string())

            if (mode == "exit"):
                ws.send(disconnect_message())
                ws.close()
                break
            elif (mode == "transaction"):
                print ("beginning transaction...")

                sk, pk = private_key, public_key

                address = input("What address do you want to send to?: ")
                amnt = float(input("How much would you like to send?: "))

                pk_hex = base64.b16encode(pk.to_string()).decode('utf-8')
                balance = get_balance(pk_hex)

                commission = amnt * 0.01
                total_amnt = amnt + commission

                print ("total amnt being sent is " + str(total_amnt))

                if ((balance - total_amnt) < 0):
                    print ("can't send payment. Insufficient funds")
                else:
                    transaction = create_transaction(sk, pk, amnt, address)

                    transaction_data = {
                        "message_type": "transaction",
                        "data": str(transaction)
                    }

                    transaction_data_json = json.dumps(transaction_data)

                    ws.send(transaction_data_json)

            elif (mode == "address"):
                pk_hex = base64.b16encode(public_key.to_string()).decode('utf-8')
                print ("Your address below:")
                print (pk_hex)

            elif (mode == "nodes"):
                command_data = {
                    "message_type": "command",
                    "command": "get_nodes"
                }

                command_data_json = json.dumps(command_data)

                ws.send(command_data_json)
                time.sleep(1)
            elif (mode == "balance"):
                pk_hex = base64.b16encode(public_key.to_string()).decode('utf-8')
                balance = get_balance(pk_hex)
                print ("Your balance is " + str(balance))

        print ("thread terminating")

    client_thread = threading.Thread(target=run)
    client_thread.start()

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:5000/wallet",
        on_message = on_message,
        on_error = on_error,
        on_close = on_close
    )

    blockchain = load_blockchain()

    ws.on_open = on_open
    ws.run_forever()
