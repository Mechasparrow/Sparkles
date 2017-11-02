import json
import hashlib
import base64

import sys

sys.path.append("../CryptoWork")

import crypto_key_gen

class Transaction:

    def __init__(self, sender, address, amnt, private_key):
        self.private_key = private_key
        self.sender_pub_key = sender
        self.address = address
        self.amnt = amnt

        self.raw_transaction = {
            "from_pub_key": self.sender_pub_key,
            "to_address": self.address,
            "amnt": self.amnt,
        }

        raw_transaction_json = json.dumps(self.raw_transaction)
        print (raw_transaction_json)

        self.raw_transaction_hash = hashlib.sha256(raw_transaction_json.encode('utf-8')).hexdigest()

        #print (self.raw_transaction_hash)

    def view_transaction(self):

        signature = base64.b16encode(self.private_key.sign(self.raw_transaction_hash.encode('utf-8'))).decode('utf-8')

        new_transaction = self.raw_transaction.copy()
        new_transaction.update({"signature": signature})

        return new_transaction

    def verify_transaction(self, signature):

        pk = crypto_key_gen.from_public_hex(self.sender_pub_key)
        decoded_signature = base64.b16decode(signature)

        print(crypto_key_gen.validate_signature(pk, decoded_signature, self.raw_transaction_hash))
