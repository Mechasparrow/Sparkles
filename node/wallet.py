from transaction import Transaction

print ("Hello wecome to Spark wallet v1 what would you like to do")
print("- check balance")
print("- create transaction")
print("- create address")

address = input ("Input the address to send to: ")

transaction = Transaction(address, 1, "123asdf")

print (transaction.view_transaction())

print (transaction)

