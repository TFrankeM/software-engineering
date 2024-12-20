from user import User

class Customer(User):
    """
    A class representing a customer in the system.
    """
    def __init__(self, name, email, password, address=None, anonymous_profile=True, coins=0):
        """
        Initialize a new customer.

        Parameters:
            name (str): The name of the customer.
            email (str): The email address of the customer.
            address (str): The address of the customer.
            password (str): The password of the customer.
            profile_picture_path (str): The path to the customer's profile picture.
            anonymous_profile (bool): Whether the customer's profile is anonymous (default is True).
            coins (float): Numbers of coins the customer have 
            
        """
        super().__init__(name, email, password, address, anonymous_profile)
        self.coins = coins
        self.reviews = []
        self.orders = []
    
    def add_coins(self, amount):
        """
        Add coins to the customer's balance.

        Parameters:
            amount (int): The number of coins to add.
        """
        self.coins += amount
    
    def get_coins(self):
        """
        Return the number of coins the customer has.

        Returns:
            int: The number of coins the customer has.
        """
        return self.coins
    
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
    

    