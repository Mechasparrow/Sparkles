from blockchain import BlockChain

import sys

sys.path.append("../block")

from block import Block

genesis_block = Block.load_from_file('./genesis_block/genesis_block.json')

blocks = [genesis_block]

blockchain = BlockChain(blocks)
print (blockchain)

blockchain_json = blockchain.__str__()

new_blockchain = BlockChain.from_json(blockchain_json)
print (new_blockchain)
