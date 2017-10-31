from transaction import Transaction

import sys

sys.path.append("../CryptoWork")

import crypto_key_gen

address = input ("Input the address to send to: ")

sender = ""

pk = "meh"

transaction = Transaction(sender, address, 10, pk)

print (transaction.view_transaction())
