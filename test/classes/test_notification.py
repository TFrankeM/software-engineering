from datetime import datetime, timedelta
import unittest
import sys, os
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src/classes")))
from notification import Notification  

class TestNotification(unittest.TestCase):
    def setUp(self):
        """
        Setup method to initialize the test environment.
        This method is called before each test case.
        """
        self.user_id = "user_123"
        self.message = "This is a test notification."
        self.notification = Notification(self.user_id, self.message)

    def test_notification_creation(self):
        """
        Test the creation of a Notification instance.
        Checks whether the attributes are correctly assigned.
        """
        self.assertIsNotNone(self.notification.id)
        self.assertEqual(self.notification.user_id, self.user_id)
        self.assertEqual(self.notification.message, self.message)
        self.assertIsInstance(self.notification.notification_date, datetime)

    def test_notification_id_is_uuid(self):
        """
        Test that the id attribute is a valid UUID.
        """
        self.assertIsInstance(self.notification.id, uuid.UUID)

    def test_notification_date_default(self):
        """
        Test that the notification_date defaults to the current time.
        """
        now = datetime.now()
        self.assertAlmostEqual(self.notification.notification_date, now, delta=timedelta(seconds=1))

    def test_notification_date_custom(self):
        """
        Test setting a custom notification_date.
        """
        custom_date = datetime(2023, 1, 1, 12, 0, 0)
        notification = Notification(self.user_id, self.message, custom_date)
        self.assertEqual(notification.notification_date, custom_date)

    def test_notification_repr(self):
        """
        Test the __repr__ method.
        Ensure that the string representation of the notification is correct.
        """
        expected_repr = f"<Notification(id={self.notification.id}, user_id={self.user_id}, message={self.message}, notification_date={self.notification.notification_date})>"
        self.assertEqual(repr(self.notification), expected_repr)

if __name__ == "__main__":
    unittest.main()
