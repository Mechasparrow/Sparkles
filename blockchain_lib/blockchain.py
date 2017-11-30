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
        block = None

        for b in self.blocks:
            if b.hash == hash:
                block = b

        return block

    def find_by_index(self, idx):

        block = None

        for b in self.blocks:
            if b['index'] == str(idx):
                block = b

        return block

    def block_sort(blocks):
        sorted_blocks = sorted(blocks, key = lambda x: int(x.index))
        return sorted_blocks

    def valid_block(block, NUM_OF_ZEROS = 4):
        if (str(block.hash[0:NUM_OF_ZEROS]) == '0' * NUM_OF_ZEROS):
            return True
        else:
            return False

    def validate_chain(self):

        valid_block = True
        prev_block_hash = "None"

        for block in self.blocks:
            if (block.index == 0):
                if (block.prev_hash == prev_block_hash and BlockChain.valid_block(block)):
                    prev_block_hash = block.hash
                    continue
                else:
                    valid_block = False
                    break
            else:
                if (block.prev_hash == prev_block_hash and BlockChain.valid_block(block)):
                    prev_block_hash = block.hash
                else:
                    valid_block = False
                    break

        return valid_block

    def sync_blockchain(chain_1, chain_2):

        chain_1_valid = chain_1.validate_chain()
        chain_2_valid = chain_2.validate_chain()

        if (chain_1_valid == True and chain_2_valid == False):
            return chain_1
        elif (chain_1_valid == False and chain_2_valid == True):
            return chain_2
        else:
            print ("comparing")

            if len(chain_1) > len(chain_2):
                return chain_1
            elif len(chain_2) > len(chain_1):
                return chain_2
            else:
                return chain_1


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

    def __len__(self):
        return len(self.blocks)

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

        blockchain.blocks = BlockChain.block_sort(blockchain.blocks)

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
