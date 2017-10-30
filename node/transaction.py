class Transaction:

    def __init__(self, address, amnt, private_key):
        self.address = address
        self.amnt = amnt

    def view_transaction(self):

        transaction = {
            "address": self.address,
            "amnt": self.amnt
        }

        return transaction
