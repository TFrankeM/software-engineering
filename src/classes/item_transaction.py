class ItemTransaction:
    """
    Class representing an item within a transaction.
    """
    def __init__(self, transaction_id, product_id, quantity, price):
        """
        Initialize a new item transaction.

        Parameters:
            transaction_id (str): The ID of the transaction this item belongs to.
            product_id (str): The ID of the product.
            quantity (int): The quantity of the product purchased.
            price (float): The price of the product.
        """
        
        self.transaction_id = transaction_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price


    def __repr__(self):
        return f"<ItemTransaction(transaction_id={self.transaction_id}, product_id={self.product_id}, quantity={self.quantity}, price={self.price})>"
