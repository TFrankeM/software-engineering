from user import User

class Customer(User):
    """
    A class representing a customer in the system.
    """
    def __init__(self, name, email, address, password, profile_picture_path=None, anonymous_profile=True):
        """
        Initialize a new customer.

        Parameters:
            name (str): The name of the customer.
            email (str): The email address of the customer.
            address (str): The address of the customer.
            password (str): The password of the customer.
            profile_picture_path (str): The path to the customer's profile picture.
            anonymous_profile (bool): Whether the customer's profile is anonymous (default is True).
        """
        super().__init__(name, email, address, password, profile_picture_path, anonymous_profile)
        self.reviews = []
        self.orders = []
    
    
    def add_review(self, review):
        """
        Add a review to the customer's list of reviews.

        Parameters:
            review (Review): The review to add.
        """
        self.reviews.append(review)
    
    def add_order(self, order):
        """
        Add an order to the customer's list of orders.

        Parameters:
            order (Order): The order to add.
        """
        self.orders.append(order)
    
    def get_reviews(self):
        """
        Return a list of reviews written by the customer.

        Returns:
            list: A list of reviews written by the customer.
        """
        return self.reviews
    
    def get_orders(self):
        """
        Return a list of orders placed by the customer.

        Returns:
            list: A list of orders placed by the customer.
        """
        return self.orders
    

    