from ecdsa import SigningKey, SECP256k1

def generate_key():
    sk = SigningKey.generate(curve=SECP256k1)
    return sk

def get_public_key(secret_key):
    return secret_key.get_verifying_key()

def sign_message(sk, message):
    return sk.sign(message)

def save_key(key, path):
    key_pem = key.to_pem()
    pem = open (path, 'wb')
    pem.write(key_pem)
    pem.close()
    print ("file saved")
