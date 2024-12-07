import unittest
import sys, os
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src/classes")))
from favorite_machine import FavoriteMachine  # Importe a classe favorita da máquina


class TestFavoriteMachine(unittest.TestCase):
    def setUp(self):
        """
        Setup method to initialize the test environment.
        This method is called before each test case.
        """
        self.user_id = "user_789"
        self.machine_id = "machine_101"
        self.favorite_machine = FavoriteMachine(self.user_id, self.machine_id)

    def test_favorite_machine_creation(self):
        """
        Test the creation of a FavoriteMachine instance.
        Checks whether the attributes are correctly assigned.
        """
        self.assertIsNotNone(self.favorite_machine.id)
        self.assertEqual(self.favorite_machine.user_id, self.user_id)
        self.assertEqual(self.favorite_machine.machine_id, self.machine_id)

    def test_favorite_machine_id_is_uuid(self):
        """
        Test that the id attribute is a valid UUID.
        """
        self.assertIsInstance(self.favorite_machine.id, uuid.UUID)

    def test_favorite_machine_repr(self):
        """
        Test the __repr__ method.
        Ensure that the string representation of the favorite machine is correct.
        """
        expected_repr = f"<FavoriteMachine(id={self.favorite_machine.id}, user_id={self.user_id}, machine_id={self.machine_id})>"
        self.assertEqual(repr(self.favorite_machine), expected_repr)


if __name__ == "__main__":
    unittest.main()
