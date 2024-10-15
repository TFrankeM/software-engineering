from user import User

class Seller(User):
    """
    A class representing a seller in the system.
    """
    def __init__(self, name, email, password, address=None, anonymous_profile=True):
        """
        Initialize a new seller.

        Parameters:
            name (str): The name of the seller.
            email (str): The email address of the seller.
            address (str): The address of the seller.
            password (str): The password of the seller.
            profile_picture_path (str): The path to the seller's profile picture.
            anonymous_profile (bool): Whether the seller's profile is anonymous (default is True).
        """
        super().__init__(name, email, password, address, anonymous_profile)
        self.products = []
        self.orders = []
    
    
    def add_product(self, product):
        """
        Add a product to the seller's list of products.

        Parameters:
            product (Product): The product to add.
        """
        self.products.append(product)
    
    def add_order(self, order):
        """
        Add an order to the seller's list of orders.

        Parameters:
            order (Order): The order to add.
        """
        self.orders.append(order)
    
    def get_products(self):
        """
        Return a list of products listed by the seller.

        Returns:
            list: A list of products listed by the seller.
        """
        return self.products
    
    def get_orders(self):
        """
        Return a list of orders placed with the seller.

        Returns:
            list: A list of orders placed with the seller.
        """
        return self.orders


