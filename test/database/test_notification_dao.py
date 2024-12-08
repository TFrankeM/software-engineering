from datetime import datetime
import pandas as pd
import unittest
import sqlite3
import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src/classes")))
from notification import Notification

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src/database")))
from notification_dao import NotificationDAO

class TestNotificationDAO(unittest.TestCase):
    def setUp(self):
        """
        Setup method to initialize the test environment.
        This method is called before each test case.
        """
        self.connection = sqlite3.connect(":memory:")  # Usar um banco de dados em memória para testes
        self.dao = NotificationDAO(self.connection)
        self.dao.create_table()
        self.user_id = "user_123"
        self.message = "This is a test notification."
        self.notification = Notification(self.user_id, self.message)

    def test_create_table(self):
        """
        Test the creation of the notifications table.
        """
        self.dao.create_table()
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='notifications'")
        self.assertIsNotNone(cursor.fetchone())

    def test_insert_notification(self):
        """
        Test inserting a notification into the database.
        """
        self.dao.insert_notification(self.notification)
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM notifications WHERE id = ?", (str(self.notification.id),))
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], self.user_id)
        self.assertEqual(result[2], self.message)
        self.assertAlmostEqual(datetime.strptime(result[3], "%Y-%m-%d %H:%M:%S.%f"), self.notification.notification_date, delta=pd.Timedelta(seconds=1))

    def test_get_notifications_by_user(self):
        """
        Test retrieving notifications by user.
        """
        self.dao.insert_notification(self.notification)
        notifications_df = self.dao.get_notifications_by_user(self.user_id)
        self.assertIsInstance(notifications_df, pd.DataFrame)
        self.assertGreaterEqual(len(notifications_df), 1)
        self.assertEqual(notifications_df.iloc[0]['user_id'], self.user_id)
        self.assertEqual(notifications_df.iloc[0]['message'], self.message)
        self.assertAlmostEqual(notifications_df.iloc[0]['notification_date'], self.notification.notification_date, delta=pd.Timedelta(seconds=1))

    def tearDown(self):
        """
        Teardown method to clean up after each test case.
        This method is called after each test case.
        """
        self.connection.close()

if __name__ == "__main__":
    unittest.main()
