import uuid
from datetime import datetime

class Notification:
    """
    Class representing a notification sent to a user.
    """
    def __init__(self, user_id, message, notification_date=None):
        """
        Initialize a new notification instance.

        Parameters:
            user_id (str): The ID of the user receiving the notification.
            message (str): The message to be sent to the user.
            notification_date (datetime, optional): The date when the notification was created (default is current time).
        """
        self.id = uuid.uuid4()  # Unique ID for the notification
        self.user_id = user_id  # ID of the user receiving the notification
        self.message = message  # The content of the notification
        self.notification_date = notification_date or datetime.now()  # Timestamp of when the notification was created

    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, message={self.message}, notification_date={self.notification_date})>"
