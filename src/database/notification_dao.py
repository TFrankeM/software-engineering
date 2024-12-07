import pandas as pd
import sqlite3
import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../classes")))
from notification import Notification

class NotificationDAO:
    """
    Data Access Object (DAO) for managing notifications in the database.
    """
    def __init__(self, db_connection):
        """
        Initialize the NotificationDAO with a database connection.

        Parameters:
            db_connection (sqlite3.Connection): A connection object to the SQLite database.
        """
        self.connection = db_connection


    def create_table(self):
        """
        Create the notifications table in the database if it doesn't already exist.
        """
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                message TEXT NOT NULL,
                notification_date TEXT NOT NULL
            );
        """)
        self.connection.commit()


    def insert_notification(self, notification):
        """
        Insert a notification into the database.

        Parameters:
            notification (Notification): The Notification object to be inserted into the database.
        """
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO notifications (id, user_id, message, notification_date)
            VALUES (?, ?, ?, ?)
        """, (str(notification.id), notification.user_id, notification.message, notification.notification_date))
        self.connection.commit()


    def get_notifications_by_user(self, user_id):
        """
        Retrieve all notifications for a specific user.

        Parameters:
            user_id (str): The ID of the user whose notifications are being fetched.

        Returns:
            list: A list of Notification objects for the given user.
        """
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT id, user_id, message, notification_date FROM notifications WHERE user_id = ?
        """, (user_id,))
        rows = cursor.fetchall()

       # Convert the rows into a DataFrame
        notifications_df = pd.DataFrame(rows, columns=["id", "user_id", "message", "notification_date"])
        
        # Convert the notification_date column to datetime
        notifications_df['notification_date'] = pd.to_datetime(notifications_df['notification_date'])

        return notifications_df
