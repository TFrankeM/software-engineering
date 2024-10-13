from datetime import datetime
import uuid


class Review:
    """
    Class to represent a review made by a user for a product or vending machine.
    """

    MAX_COMMENT_LENGTH = 250

    def __init__(self, user_id, recipient_id, rating, comment=None):
        """
        Initialize the review with id, user_id, recipient_id, rating, and an optional comment.
        
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
        self.recipient_id = recipient_id
        self.rating = self.validate_rating(rating)
        self.comment = self.validate_comment(comment)

    def __str__(self):
        """
        Return a string representation of the review.
        """
        return f"Review by User {self.user_id} for {self.recipient_id}: {self.rating}/5 - {self.comment}"


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


    def save_to_db(self, connection):
        """
        Save the review to the SQLite database.

        Parameters:
        -----------
        connection (sqlite3.Connection): Connection to the SQLite database.
        """
        with connection:
            connection.execute("""
                INSERT INTO reviews (id, date, comment, rating, user_id, recipient_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (str(self.id), self.date, self.comment, self.rating, self.user_id, self.recipient_id))

