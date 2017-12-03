import json
import hashlib
import base64

import sys

sys.path.append("../CryptoWork")

import crypto_key_gen

class Transaction:

    def __init__(self, sender, address, amnt, note = "", private_key=None, signature = None):
        self.sender_pub_key = sender
        self.address = address
        self.amnt = amnt
        self.note = note
        self.signature = signature

        if (signature == None):
            self.signature = self.generate_signature(private_key)

    def __dict__(self):
        transaction_dict = {
            "sender_pub_key": str(self.sender_pub_key),
            "address": str(self.address),
            "amnt": str(self.amnt),
            "note": str(self.note),
            "signature": str(self.signature)
        }

        return transaction_dict

    def __eq__(self, other):
        return self.signature == other.signature

    def __str__(self):
        transaction_dict = self.__dict__()
        transaction_json = json.dumps(transaction_dict)
        return transaction_json

    def get_hash(self):
        hash_pre_string = str(self.sender_pub_key) + str(self.address) + str(self.amnt) + str(self.note)
        m = hashlib.sha256()
        m.update(hash_pre_string.encode('utf-8'))
        return m.hexdigest()

    def generate_signature(self, private_key):
        hash_string = self.get_hash().encode('utf-8')
        signature = crypto_key_gen.sign_message(private_key, hash_string)
        b16_signature = base64.b16encode(signature).decode('utf-8')
        return b16_signature

    def validate_transaction(self):
        signature = base64.b16decode(self.signature)
        transaction_hash = self.get_hash()
        public_key = crypto_key_gen.from_public_hex(self.sender_pub_key)
        signature_valid = crypto_key_gen.validate_signature(public_key, signature, transaction_hash)
        return signature_valid

    def from_json(transaction_json):
        transaction_dict = json.loads(transaction_json)
        return Transaction.from_dict(transaction_dict)

    def from_dict(transaction_dict):
        return Transaction(sender=transaction_dict['sender_pub_key'],address=transaction_dict['address'], amnt = transaction_dict['amnt'], note = transaction_dict['note'], signature = transaction_dict['signature'])
