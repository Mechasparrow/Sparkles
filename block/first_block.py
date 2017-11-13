from block import Block
import datetime as date

genesis_block_data = {}
genesis_block_data['index'] = 0
genesis_block_data['timestamp'] = date.datetime.now()
genesis_block_data['data'] = "First Block!"
genesis_block_data['prev_hash'] = None
genesis_block_data['hash'] = None
genesis_block_data['nonce'] = 0

genesis_block = Block.from_dict(genesis_block_data)

print (genesis_block)
