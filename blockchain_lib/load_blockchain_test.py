from blockchain import BlockChain

import sys

sys.path.append("../block")

from block import Block

blockchain = BlockChain.load_blockchain('./blockchain_dir/blockchain.json')

print (blockchain)
