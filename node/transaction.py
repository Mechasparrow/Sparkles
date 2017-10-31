class Transaction:

    def __init__(self, sender, address, amnt, private_key):
        self.private_key = private_key
        self.sender = sender
        self.address = address
        self.amnt = amnt

    def view_transaction(self):

        transaction = {
            "from_address": self.sender,
            "to_address": self.address,
            "amnt": self.amnt,
            "signature": self.private_key.sign(self)
        }

        return transaction
