from block import Block

genesis_block = Block.load_from_file('./genesis_block.json')

print (genesis_block)
