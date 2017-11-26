import json
import hashlib
import base64

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
            "chain": self.blocks
        }

        return chain_dict

    def __str__(self):
        chain_dict = self.__dict__()
        chain_json = json.dumps(chain_dict)
        return chain_json
