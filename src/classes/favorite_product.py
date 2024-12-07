import uuid

class FavoriteProduct:
    """
    Class representing a favorite product of a user.
    """
    def __init__(self, user_id, product_id):
        """
        Initialize a new favorite product instance.

        Parameters:
            user_id (str): The ID of the user who favorited the product.
            product_id (str): The ID of the product that was favorited.
        """
        self.id = uuid.uuid4()  # Unique ID for the favorite record
        self.user_id = user_id
        self.product_id = product_id

    def __repr__(self):
        return f"<FavoriteProduct(id={self.id}, user_id={self.user_id}, product_id={self.product_id})>"
