import websocket
import _thread
import time
import json

import sys

sys.path.append("../CryptoWork")

from transaction import Transaction
import crypto_key_gen

def on_message(ws, message):
    message_decoded = json.loads(message)

    if (message_decoded['message_type'] == "message"):
        print (message_decoded['message'])


def on_error(ws, error):
    print (error)

def on_close(ws):
    print ("### closed ###")

def create_transaction(amnt, address):



    pass

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
                amnt = input("How much would you like to send?: ")
                address = input("What is the address of the recipient?: ")

                transaction_data = {
                    "message_type": "transaction",
                    "data": {
                        "amnt": amnt,
                        "address": address
                    }
                }

                transaction_json = json.dumps(transaction_data)
                ws.send(transaction_json)



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

    ws.on_open = on_open
    ws.run_forever()
