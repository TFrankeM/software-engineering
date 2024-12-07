from datetime import datetime
import uuid

class MoneyDeposit:
    """
    Class to represent a money deposit made by a customer in the system.
    """

    MAX_AMOUNT = 100000.0  # Maximum deposit amount allowed per transaction
    
    def __init__(self, customer_id, amount):
        """
        Initialize the money deposit with details about the transaction.

        Parameters:
            customer_id (int): ID of the customer making the deposit.
            amount (float): Amount of money being deposited.

        Raises:
            ValueError: If the amount is invalid or if the deposit_method is not recognized.
        """
        self.id = uuid.uuid4()  # Unique ID for the deposit
        self.customer_id = customer_id
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.amount = self._validate_amount(amount)

    def _validate_amount(self, amount):
        """
        Validate the deposit amount.

        Parameters:
            amount (float): The deposit amount to validate.

        Returns:
            float: The validated amount.

        Raises:
            ValueError: If the amount is less than or equal to zero or exceeds the maximum allowed.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")
        if amount > self.MAX_AMOUNT:
            raise ValueError(f"Deposit amount cannot exceed {self.MAX_AMOUNT}.")
        return amount

    def __str__(self):
        """
        Return a string representation of the money deposit.
        """
        return (f"Money Deposit by Customer {self.customer_id}: "
                f"Amount: {self.amount}, "
                f"Timestamp: {self.timestamp}")