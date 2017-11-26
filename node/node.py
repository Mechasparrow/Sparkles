from socketIO_client import SocketIO, LoggingNamespace

from transaction import Transaction

import sys
    
sys.path.append("../CryptoWork")

import crypto_key_gen

import json
import hashlib
import base64

#Handle incoming messages

def on_connect():
    print ('connected to backend')

def on_message_response(*args):
    message = args[0]['data']
    print (message)

socketIO = SocketIO('localhost', 8000, LoggingNamespace)

# Example transaction

sk = crypto_key_gen.generate_key()
pk = crypto_key_gen.get_public_key(sk)

pk_hex = base64.b16encode(pk.to_string()).decode('utf-8')

sk2 = crypto_key_gen.generate_key()
pk2 = crypto_key_gen.get_public_key(sk2)

pk2_hex = base64.b16encode(pk2.to_string())
address_hash = hashlib.sha256(pk2_hex).hexdigest()

sparkle_amnt = 2

transaction = Transaction(pk_hex, address_hash, sparkle_amnt, private_key = sk)
transaction_string = str(transaction)

socketIO.emit("transaction", transaction_string)
