import uuid
from review import Review


class Product:
    """
        Class representing a product in the vending machine system.
    """

    def __init__(self, name, description, price, quantity=0, reviews=None):
        """
            Initialize a Product instance.

        Parameters:
            name (str): Name of the product.
            description (str): Description of the product.
            price (float): Price of the product.
            quantity (int): Quantity of the product in stock.
            reviews (list of Review, optional): List of reviews associated with the product.
        """
        self.id = uuid.uuid4()
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.reviews = reviews if reviews is not None else []  # Initialize reviews as an empty list if not provided


    def add_review(self, review):
        """
            Add a review to the product.

        Parameters:
            review (Review): A review object to be added to the product.
        """
        if isinstance(review, Review):
            self.reviews.append(review)
        else:
            raise ValueError("Invalid review object")


    def apply_discount(self, percentage):
        """
            Apply a discount to the product's price.

        Parameters:
            percentage (float): The percentage of discount to be applied.
        """
        if 0 <= percentage <= 100:
            discount = self.price * (percentage / 100)
            self.price -= discount
        else:
            raise ValueError("Discount percentage must be between 0 and 100")


    def __str__(self):
        """
            Return a string representation of the product.
        """
        return f"Product({self.name}, Price: {self.price}, Quantity: {self.quantity})"
