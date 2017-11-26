import json
import hashlib
import base64

import sys

sys.path.append("../block")

from block import Block

class BlockChain:

    def __init__(self, chain):
        self.blocks = chain

    def find_by_hash(self,hash):
        
        pass

    def find_by_index(self, idx):

        pass

    def validate_chain(self):

        pass

    def check_balance(self, spk_addr):

        pass

    def __dict__(self):
        chain_dict = {
        }

        for block in self.blocks:
            chain_dict[block.index] = str(block)

        return chain_dict

    def __str__(self):
        chain_dict = self.__dict__()
        chain_json = json.dumps(chain_dict)
        return chain_json

    def add_block(self, block):

        pass

    def save_blockchain(self, path):
        blockchain_json = self.__str__()
        blockchain_file = open(path, 'wb')
        blockchain_file.write(blockchain_json.encode('utf-8'))
        blockchain_file.close()

        print ("saved blockchain")

    def load_blockchain(path):

        blockchain_file = open(path, 'rb')

        blockchain_json = blockchain_file.read().decode('utf-8')

        blockchain = BlockChain.from_json(blockchain_json)

        return blockchain

    def from_dict(blockchain_dict):

        blocks = []

        for block_index in blockchain_dict.keys():
            block_string = blockchain_dict[block_index]
            block = Block.from_json(block_string)
            blocks.append(block)

        blockchain = BlockChain(blocks)
        return blockchain

    def from_json(blockchain_json):

        blockchain_dict = json.loads(blockchain_json)
        blockchain = BlockChain.from_dict(blockchain_dict)

        return blockchain
