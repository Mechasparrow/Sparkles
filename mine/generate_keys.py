import sys

sys.path.append("../CryptoWork")

import crypto_key_gen

print ("generating new keys in the /keys folder...")

secret_key = crypto_key_gen.generate_key()

public_key = crypto_key_gen.get_public_key(secret_key)

crypto_key_gen.save_key(public_key, "./keys/public.pem")
crypto_key_gen.save_key(secret_key, "./keys/secret.pem")
