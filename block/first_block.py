from block import Block
import hashlib
import datetime as date

genesis_block_data = {}
genesis_block_data['index'] = 0
genesis_block_data['timestamp'] = date.datetime.now()
genesis_block_data['data'] = "First Block!"
genesis_block_data['prev_hash'] = None
genesis_block_data['hash'] = None
genesis_block_data['nonce'] = 0

def header_string(index, prev_hash, data, timestamp, nonce):
    return str(index) + str(prev_hash) + str(data) + str(timestamp) + str(nonce)

def generate_hash(header_string):
    sha = hashlib.sha256()
    sha.update(header_string.encode('utf-8'))
    return sha.hexdigest()

def mine(block_dict, NUM_ZEROS=4):
    mine_block_dict = dict.copy(block_dict)

    mine_block_dict['nonce'] = int(mine_block_dict['nonce'])

    while True:

        block_header_string = header_string(mine_block_dict['index'], mine_block_dict['prev_hash'], mine_block_dict['data'], mine_block_dict['timestamp'], mine_block_dict['nonce'])
        block_hash = generate_hash(block_header_string)

        print (block_hash)

        if (str(block_hash[0:NUM_ZEROS]) == '0' * NUM_ZEROS):
            break

        mine_block_dict['nonce'] = mine_block_dict['nonce'] + 1

    return mine_block_dict

genesis_block_data = mine(genesis_block_data)


genesis_block = Block.from_dict(genesis_block_data)
print (genesis_block)
print (genesis_block.create_self_hash())
