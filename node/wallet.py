from transaction import Transaction
import base64

import sys

sys.path.append("../CryptoWork")

import crypto_key_gen

sk = crypto_key_gen.generate_key()
pk = crypto_key_gen.get_public_key(sk)

pk_hex = base64.b16encode(pk.to_string()).decode('utf-8')

sk2 = crypto_key_gen.generate_key()
pk2 = crypto_key_gen.get_public_key(sk2)

pk2_hex = base64.b16encode(pk2.to_string()).decode('utf-8')

transaction = Transaction(pk_hex, pk2_hex, 10, sk)
print("\n")
transaction_info = transaction.view_transaction()
print()
