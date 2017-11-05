from transaction import Transaction
import base64

import sys

sys.path.append("../CryptoWork")

import crypto_key_gen

sender = "abcdfef"

address = "catz"

sk = crypto_key_gen.generate_key()
pk = crypto_key_gen.get_public_key(sk)

pk_hex = base64.b16encode(pk.to_string()).decode('utf-8')

transaction = Transaction(pk_hex, address, 10, sk)
print (transaction.validate_transaction())
