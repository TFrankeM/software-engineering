from datetime import datetime
import uuid


class Review:
    """
    Class to represent a review made by a user for a product or vending machine.
    """

    def __init__(self, user_id, recipient_id, rating, comment=None):
        """
        Initialize the review with id, user_id, recipient_id, rating, and an optional comment.
        
        Parameters:
        -----------
        user_id (int): ID of the user who made the review.
        recipient_id (int): ID of the recipient being reviewed.
        rating (int): Rating provided by the user (0 to 5).
        comment (str, optional): Optional comment provided by the user (default is None).
        """
        self.id = uuid.uuid4()
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.comment = comment
        self.rating = rating
        self.user_id = user_id
        self.recipient_id = recipient_id


    def __str__(self):
        """
        Return a string representation of the review.
        """
        return f"Review by User {self.user_id} for {self.recipient_id}: {self.rating}/5 - {self.comment}"


    def validate_rating(self):
        """
        Validate if the rating is between 0 and 5.
        """
        if 0 <= self.rating <= 5:
            return True
        else:
            return False


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

