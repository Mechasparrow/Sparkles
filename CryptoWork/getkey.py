import rsa_crypto

key_name = input("Enter name of private key file: ")
private_key = rsa_crypto.read_from_file(key_name)
print (rsa_crypto.serialize_key(private_key))
