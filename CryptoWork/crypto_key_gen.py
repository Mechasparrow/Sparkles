from ecdsa import SigningKey, VerifyingKey, SECP256k1
from ecdsa.keys import BadSignatureError
import base64

def generate_key():
    sk = SigningKey.generate(curve=SECP256k1)
    return sk

def get_public_key(secret_key):
    return secret_key.get_verifying_key()

def from_public_hex(public_hex):
    bin_string = base64.b16decode(public_hex)
    pk = VerifyingKey.from_string(bin_string, curve=SECP256k1)
    return pk

def validate_signature(public_key, signature, message):

    try:
        return public_key.verify(signature, message.encode())
    except BadSignatureError as e:
        return False

def sign_message(sk, message):
    return sk.sign(message)

def save_key(key, path):
    key_pem = key.to_pem()
    pem = open (path, 'wb')
    pem.write(key_pem)
    pem.close()
    print ("file saved")
