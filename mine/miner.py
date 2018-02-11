import threading
from threading import Thread
import time
import json
import random

import copy

import hashlib
import datetime as date

import sys

sys.path.append("../CryptoWork")
sys.path.append("../block")
sys.path.append("../node")
sys.path.append("../blockchain_lib")
sys.path.append("../p2p-networking")

from transaction import Transaction
from blockchain import BlockChain
from block import Block
from reward import Reward
import crypto_key_gen
import base64

def header_string(index, prev_hash, data, timestamp, nonce):
    return str(index) + str(prev_hash) + str(data) + str(timestamp) + str(nonce)
def generate_hash(header_string):

    sha = hashlib.sha256()
    sha.update(header_string.encode('utf-8'))
    return sha.hexdigest()

class BlockMiner(threading.Thread):

    def __init__(self, transaction, blockchain, miner_address, miner_secret):
        threading.Thread.__init__(self)

        self.stop_mining = False
        self.stop_reason = ""

        self.is_miner_active = True

        # Setup block info
        self.block = None
        self.blockchain = blockchain
        self.transaction = transaction

        # Get miner crypto info
        self.miner_address = miner_address
        self.miner_secret = miner_secret

    def run(self):
        self.mine_block()
        self.is_miner_active = False

    def mine_block(self, NUM_ZEROS = 4):

        self.create_start_block(self.transaction)

        mine_block_dict = dict.copy(self.unmined_block_dict)

        mine_block_dict['nonce'] = int(mine_block_dict['nonce'])

        while not self.stop_mining:

            block_header_string = header_string(mine_block_dict['index'], mine_block_dict['prev_hash'], mine_block_dict['data'], mine_block_dict['timestamp'], mine_block_dict['nonce'])
            block_hash = generate_hash(block_header_string)

            print (block_hash)

            if (str(block_hash[0:NUM_ZEROS]) == '0' * NUM_ZEROS):
                mine_block_dict['hash'] = block_hash
                break

            mine_block_dict['nonce'] = mine_block_dict['nonce'] + 1

        if (self.stop_mining == True):

            if (self.stop_reason == "block_conflict"):
                print (self.stop_reason)
                self.block = None
                return
            elif (self.stop_reason == "remine"):
                print ("REMINE")
                self.restart_mining()

        self.block = Block.from_dict(mine_block_dict)

    def create_start_block(self, transaction):
        iteration = len(self.blockchain.blocks)

        prev_block = self.blockchain.blocks[iteration - 1]

        reward = Reward(self.miner_address, self.transaction.amnt, block_iteration = iteration, private_key = self.miner_secret)

        data = json.dumps([str(transaction), str(reward)])

        block_data = {}
        block_data['index'] = iteration
        block_data['timestamp'] = date.datetime.now()
        block_data['data'] = str(data)
        block_data['prev_hash'] = prev_block.hash
        block_data['hash'] = None
        block_data['nonce'] = 0

        self.unmined_block_dict = block_data

    def stop(self):
        self.stop_mining = True
        self.is_miner_active = False
        pass

    def restart_mining(self):
        self.is_miner_active = True
        self.stop_mining = False

        self.mine_block()

        pass

    def intercept_block(self, block, blockchain):

        self.blockchain = blockchain
        print ("INTERCEPTION")



        try:
            block_data = json.loads(json.loads(block.data)[0])

            transaction_signature = block_data['signature']

            our_transaction_signature = self.transaction.signature

            if (transaction_signature == our_transaction_signature):
                print ("WE HAVE A BLOCK CONFLICT")
                self.stop_reason = "block_conflict"
                self.stop()
            else:
                print ("Nothing to worry about. Might have to remine")
                self.stop_reason = "remine"
                self.stop()

            print ("Signature:" + block_data['signature'])
        except Exception as err:
            print (err)



    def is_active(self):
        return self.is_miner_active

    def join(self):
        threading.Thread.join(self)
        return self.block
