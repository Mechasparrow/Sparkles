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

    raw_transaction = dict.copy(transaction)
    raw_transaction.pop('signature', None)



    raw_transaction_json = json.dumps(raw_transaction)
    print(raw_transaction_json)
    raw_transaction_hash = hashlib.sha256(raw_transaction_json.encode('utf-8')).hexdigest()


    verify_transaction(raw_transaction['from_pub_key'], raw_transaction_hash, transaction['signature'])

    print (raw_transaction_hash)

def verify_transaction(public_key_base, raw_transaction_hash, signature):
    pk = crypto_key_gen.from_public_hex(public_key_base)
    decoded_signature = base64.b16decode(signature)

    print(crypto_key_gen.validate_signature(pk, decoded_signature, raw_transaction_hash))

socketIO = SocketIO('http://localhost', 8000, LoggingNamespace)

socketIO.on('transaction_response', on_transaction_response)
socketIO.wait()
