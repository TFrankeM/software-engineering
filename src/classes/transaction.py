from datetime import datetime
import uuid


class Transaction:
    """
    Class representing a transaction (purchase of product(s)) made by a customer.
    """
    def __init__(self, user_id, total_amount, transaction_date=None):
        """
        Initialize a new transaction instance.

        Parameters:
            user_id (str): The ID of the user making the transaction.
            total_amount (float): The total amount of the transaction.
            transaction_date (datetime, optional): The date of the transaction (default is current time).
        """

        self.id = uuid.uuid4()
        self.user_id = user_id
        self.total_amount = total_amount
        self.transaction_date = transaction_date or datetime.now()


    def __repr__(self):
        return f"<Transaction(id={self.id}, user_id={self.user_id}, total_amount={self.total_amount})>"
