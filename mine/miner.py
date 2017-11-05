from socketIO_client import SocketIO, LoggingNamespace


import sys

sys.path.append("../CryptoWork")
sys.path.append("../node")

import crypto_key_gen
from transaction import Transaction


import json
import hashlib
import base64

def on_transaction_response(transaction):
    transaction = Transaction.from_json(transaction)
    print (transaction.validate_transaction())

socketIO = SocketIO('http://localhost', 8000, LoggingNamespace)

socketIO.on('transaction_response', on_transaction_response)
socketIO.wait()
