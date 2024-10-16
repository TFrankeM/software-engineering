import uuid
import product
import review

class VendingMachine:
    """
    Class to represent a vending machine.
    """
    
    def __init__(self, name, location, owner_id, products=None, reviews=None):
        """
        Initialize the vending machine with a name, location, owner (seller), and optional lists of products and reviews.

        Parameters:
            name (str): Name of the vending machine.
            location (str): Location of the vending machine.
            owner_id (str): ID of the owner (seller) of the vending machine.
            products (list, optional): List of Product objects contained in the vending machine.
            reviews (list, optional): List of reviews (Review objects) for the vending machine.
        """
        self.id = uuid.uuid4()
        self.name = name
        self.location = location
        self.owner_id = owner_id  # New owner attribute
        self.products = products if products is not None else []
        self.reviews = reviews if reviews is not None else []


    def __str__(self):
        """
            Return a string representation of the vending machine.
        """
        return f"Vending Machine '{self.name}' located at {self.location} owned by {self.owner_id}"
