import rsa_crypto

key = rsa_crypto.generate_key()
key_text = rsa_crypto.serialize_key(key)
