import json
import hashlib
import base64
import math

import sys

sys.path.append("../CryptoWork")

import crypto_key_gen

class Reward:

    def __init__(self, recipient, transaction_amnt, block_iteration, private_key = None, signature = None):
        self.recipient = recipient
        self.transaction_amnt = transaction_amnt
        self.reward_amnt = 0.01 * float(transaction_amnt)
        self.block_iteration = block_iteration
        self.block_reward = float("{0:.2f}".format(50.0 / self.block_iteration))
        self.signature = signature


        if (signature == None):
            self.generate_signature(private_key)

    def __dict__(self):
        reward_dict = {
            "recipient": str(self.recipient),
            "transaction_amnt": str(self.transaction_amnt),
            "reward_amnt": str(self.reward_amnt),
            "block_reward": str(self.block_reward),
            "block_iteration": str(self.block_iteration),
            "signature": str(self.signature)
        }

        return reward_dict

    def __str__(self):
        reward_dict = self.__dict__()
        reward_json = json.dumps(reward_dict)
        return reward_json

    def from_dict(reward_dict):
        reward = Reward(reward_dict['recipient'], reward_dict['transaction_amnt'], int(reward_dict['block_iteration']), signature= reward_dict['signature'])
        reward.block_reward = float(reward_dict['block_reward'])
        return reward

    def from_json(reward_json):
        reward_dict = json.loads(reward_json)
        return Reward.from_dict(reward_dict)

    def generate_signature(self, private_key):
        hash_string = self.get_hash().encode('utf-8')
        signature = crypto_key_gen.sign_message(private_key, hash_string)
        b16_signature = base64.b16encode(signature).decode('utf-8')
        self.signature = b16_signature
        return b16_signature

    def validate_reward(self):
        signature = base64.b16decode(self.signature)
        reward_hash = self.get_hash()
        public_key = crypto_key_gen.from_publix_hex(self.sender_pub_key)
        signature_valid = crypto_key_gen.validate_signature(public_key, signature, reward_hash)
        return signature_valid

    def get_hash(self):
        hash_pre_string = str(self.recipient) + str(self.transaction_amnt)
        m = hashlib.sha256()
        m.update(hash_pre_string.encode('utf-8'))
        return m.hexdigest()
