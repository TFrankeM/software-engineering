from datetime import datetime
import uuid


class Review:
    """
    Class to represent a review made by a user for a product or vending machine.
    """

    MAX_COMMENT_LENGTH = 250

    def __init__(self, user_id, rating, comment=None, product_id=None, machine_id=None):
        """
        Initialize the review with user_id, rating, and an optional comment. Either product_id
        or machine_id must be provided, but not both.

        Parameters:
            user_id (int): ID of the user who made the review.
            recipient_id (int): ID of the recipient being reviewed.
            rating (int): Rating provided by the user (0 to 5).
            comment (str, optional): Optional comment provided by the user (default is None).

        Raises:
            ValueError: If the comment exceeds the maximum allowed length.
            ValueError: If the rating is not between 0 and 5.
        """
        self.id = uuid.uuid4()
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.user_id = user_id
        self.rating = self.validate_rating(rating)
        self.comment = self.validate_comment(comment)

        # Validate that exactly one of product_id or machine_id is provided
        if (product_id is None and machine_id is None) or (product_id is not None and machine_id is not None):
            raise ValueError("You must provide exactly one of 'product_id' or 'machine_id'.")
        
        self.product_id = product_id
        self.machine_id = machine_id


    def __str__(self):
        """
        Return a string representation of the review.
        """
        if self.product_id:
            return f"Review by User {self.user_id} for Product {self.product_id}: {self.rating}/5 - {self.comment or 'No comment'}"
        else:
            return f"Review by User {self.user_id} for Machine {self.machine_id}: {self.rating}/5 - {self.comment or 'No comment'}"

    def validate_rating(self, rating):
        """
        Validate the rating, ensuring it's between 0 and 5.
        
        Parameters:
            rating (int): Rating provided by the user (0 to 5).

        Raises:
            ValueError: If the rating is not between 0 and 5 or is not provided..
        """
        if rating is None or not isinstance(rating, int):
            raise ValueError("Rating must be an integer between 0 and 5.")
    
        if 0 <= rating <= 5:
            return rating
        else:
            raise ValueError("Rating must be between 0 and 5.")
        

    def validate_comment(self, comment):
        """
        Validate the comment, ensuring it doesn't exceed the maximum allowed length.
        
        Parameters:
            comment (str): Comment provided by the user.
        
        Raises:
            ValueError: If the comment exceeds the maximum allowed length.
        """
        if comment and len(comment) > self.MAX_COMMENT_LENGTH:
            raise ValueError(f"Comment cannot exceed {self.MAX_COMMENT_LENGTH} characters.")
        return comment


class ProductReview(Review):
    """
    Create a ProductReview class that inherits from the Review class.

    Parameters:
    - user_id (int): The ID of the user who wrote the review.
    - rating (int): The rating given by the user.
    - comment (str, optional): The comment provided by the user. Defaults to None.
    - product_id (str, optional): The ID of the product being reviewed. Defaults to None.

    """
    def __init__(self, user_id, rating, comment=None, product_id=None):
        super().__init__(user_id, rating, comment, product_id=product_id)

class MachineReview(Review):
    """Creates a MachineReview object.

    Parameters:
    - user_id (int): The ID of the user who wrote the review.
    - rating (float): The rating given by the user.
    - comment (str, optional): The comment provided by the user. Defaults to None.
    - machine_id (str, optional): The ID of the machine being reviewed. Defaults to None.

    Returns:
    - MachineReview: A MachineReview object.

    """
    def __init__(self, user_id, rating, comment=None, machine_id=None):
        super().__init__(user_id, rating, comment, machine_id=machine_id)


class ReviewFactory:
    """
    Create a review based on the given review type.

    Parameters:
    - review_type (str): The type of review. It can be either 'product' or 'machine'.
    - user_id (int): The ID of the user who created the review.
    - rating (int): The rating given to the review.
    - comment (str): The comment provided in the review.
    - product_id (int, optional): The ID of the product being reviewed. Only required if review_type is 'product'.
    - machine_id (int, optional): The ID of the machine being reviewed. Only required if review_type is 'machine'.

    Returns:
    - ProductReview or MachineReview: The created review object.

    Raises:
    - ValueError: If an invalid review_type is provided.
    """
    @staticmethod
    def create_review(review_type, user_id, rating, comment, product_id=None, machine_id=None):
        if review_type == "product":
            return ProductReview(user_id, rating, comment, product_id)
        elif review_type == "machine":
            return MachineReview(user_id, rating, comment, machine_id)
        else:
            raise ValueError("Tipo de avaliação inválido")
