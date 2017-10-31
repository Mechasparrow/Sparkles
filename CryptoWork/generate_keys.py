import crypto_key_gen
import hashlib

sk = crypto_key_gen.generate_key()
pk = crypto_key_gen.get_public_key(sk)

crypto_key_gen.save_key(sk, "./wallet/secret.pem")
crypto_key_gen.save_key(pk, "./wallet/public.pem")
