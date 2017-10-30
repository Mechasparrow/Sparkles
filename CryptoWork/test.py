import crypto_key_gen

sk = crypto_key_gen.generate_key()
pk = crypto_key_gen.get_public_key(sk)

print (pk.to_string())
