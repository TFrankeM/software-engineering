from unittest.mock import patch, MagicMock
import unittest
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from seller_flow import seller_actions

class TestSellerFlow(unittest.TestCase):

    @patch("builtins.input", side_effect=["1", "0"])  # Simulate viewing vending machines then exiting
    def test_seller_view_vending_machines(self, mock_input):
        # Setup a mock db_connection
        mock_db_connection = MagicMock()
        mock_db_connection.cursor.return_value = MagicMock()

        seller_id = "test_seller_id"
        
        # Call seller_actions and pass the mocked db_connection
        seller_actions(seller_id=seller_id, db_connection=mock_db_connection)


    @patch("builtins.input", side_effect=["TestMachine", "TestLocation", "0"])  # Simulate inserting a vending machine then exiting
    def test_seller_insert_vending_machine(self, mock_input):
        # Setup a mock db_connection
        mock_db_connection = MagicMock()
        mock_db_connection.cursor.return_value = MagicMock()

        seller_id = "test_seller_id"

        # Call seller_actions and pass the mocked db_connection
        seller_actions(seller_id=seller_id, db_connection=mock_db_connection)


    @patch("builtins.input", side_effect=["1", "0"])  # Simulate deleting a vending machine then exiting
    def test_seller_delete_vending_machine(self, mock_input):
        # Setup a mock db_connection
        mock_db_connection = MagicMock()
        mock_db_connection.cursor.return_value = MagicMock()

        seller_id = "test_seller_id"

        # Call seller_actions and pass the mocked db_connection
        seller_actions(seller_id=seller_id, db_connection=mock_db_connection)


    @patch("builtins.input", side_effect=["0"])  # Simulate exiting
    def test_seller_exit(self, mock_input):
        # Setup a mock db_connection
        mock_db_connection = MagicMock()
        mock_db_connection.cursor.return_value = MagicMock()

        seller_id = "test_seller_id"

        # Call seller_actions and pass the mocked db_connection
        seller_actions(seller_id=seller_id, db_connection=mock_db_connection)


if __name__ == "__main__":
    unittest.main()
