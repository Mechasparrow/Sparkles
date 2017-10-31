import crypto_key_gen
import hashlib

sk = crypto_key_gen.generate_key()
pk = crypto_key_gen.get_public_key(sk)

pk_string = pk.to_string()
print (pk_string)
print (hashlib.sha256(pk_string).hexdigest())
