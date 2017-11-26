from reward import Reward
import base64

import sys

sys.path.append('../CryptoWork')

import crypto_key_gen

sk = crypto_key_gen.generate_key()
pk = crypto_key_gen.get_public_key(sk)

pk_hex = base64.b16encode(pk.to_string()).decode('utf-8')

reward = Reward(pk_hex, 10, block_iteration = 100, private_key = sk)

print (reward)
