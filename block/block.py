import json
import hashlib
import base64

class Block:
    def __init__(self, index, timestamp, data, prev_hash, hash=None, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prev_hash
        self.hash = hash
        self.nonce = nonce

    def header_string(self):
        return str(self.index) + str(self.prev_hash) + str(self.data) + str(self.timestamp) + str(self.nonce)

    def create_self_hash(self):
        sha = hashlib.sha256()
        sha.update(self.header_string().encode('utf-8'))
        return sha.hexdigest()

    def __dict__(self):
        block_dict = {
            "index": str(self.index),
            "timestamp": str(self.timestamp),
            "data": str(self.data),
            "prev_hash": str(self.prev_hash),
            "hash": str(self.hash),
            "nonce": str(self.nonce)
        }

        return block_dict

    def __str__(self):
        block_dict = self.__dict__()
        block_json = json.dumps(block_dict)
        return block_json

    def from_dict(block_dict):
        block = Block(int(block_dict['index']), block_dict['timestamp'], block_dict['data'], block_dict['prev_hash'], block_dict['hash'], int(block_dict['nonce']))
        return block

    def from_json(block_json):
        block_dict = json.loads(block_json)
        block = Block.from_dict(block_dict)
        return block

    def valid_block(self):
        pass
