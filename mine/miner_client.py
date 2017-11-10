import websocket
import _thread
import time
import json

import sys

sys.path.append("../CryptoWork")
sys.path.append("../node")

from transaction import Transaction

def on_message(ws, message):
    message_decoded = json.loads(message)
    if (message_decoded['message_type'] == 'transaction'):
        transaction_json = message_decoded['data']
        transaction = Transaction.from_json(transaction_json)
        if (transaction.validate_transaction() == True):
            create_block(transaction)

def create_block(transaction):
    print ("mining block...")

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
