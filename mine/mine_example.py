import hashlib
import json

block = {
    "message": "bleh",
    "nonce": 0
}

computed = False

while not computed:

    block_string = json.dumps(block)
    block_hash = hashlib.sha256(block_string.encode('utf-8')).hexdigest()

    if (block_hash.startswith("000000")):
        computed = True


    block["nonce"] += 1
