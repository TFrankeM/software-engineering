from unittest.mock import patch, MagicMock
import unittest
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from seller_flow import (
    create_new_product,
    remove_product,
    update_product,
    view_vending_machine_details,
    view_vending_machines_basic_info,
    insert_new_vending_machine,
    delete_vending_machine,
    seller_actions
)
from product_dao import ProductDAO
from vending_machine_dao import VendingMachineDAO
from vending_machine import VendingMachine
from product import Product

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

    @patch("builtins.input", side_effect=["Product1", "Description1", "10.0", "5", "s"])
    def test_create_new_product(self, mock_input):
        # Setup
        mock_product_dao = MagicMock(spec=ProductDAO)
        mock_vending_machine = VendingMachine("TestMachine", "TestLocation", "test_seller_id")

        # Test create_new_product function
        create_new_product(mock_vending_machine, mock_product_dao)

        # Verify that the insert_product method was called
        mock_product_dao.insert_product.assert_called_once()


    @patch("builtins.input", side_effect=["1", "0"])
    def test_view_vending_machines_basic_info(self, mock_input):
        # Setup
        mock_vending_machine_dao = MagicMock(spec=VendingMachineDAO)
        mock_product_dao = MagicMock(spec=ProductDAO)
        mock_seller_id = "test_seller_id"

        # Test view_vending_machines_basic_info function
        view_vending_machines_basic_info(mock_seller_id, None, mock_vending_machine_dao, mock_product_dao)

        # Verify that the get_vending_machines_by_seller_id method was called
        mock_vending_machine_dao.get_vending_machines_by_seller_id.assert_called_once_with(mock_seller_id)
    

    @patch("builtins.input", side_effect=["TestMachine", "TestLocation", "0"])
    def test_insert_new_vending_machine(self, mock_input):
        # Setup
        mock_vending_machine_dao = MagicMock(spec=VendingMachineDAO)
        mock_seller_id = "test_seller_id"

        # Test insert_new_vending_machine function
        insert_new_vending_machine(mock_seller_id, None, mock_vending_machine_dao)

        # Verify that the insert_vending_machine method was called
        mock_vending_machine_dao.insert_vending_machine.assert_called_once()
    

    @patch("builtins.input", side_effect=["1", "0"])
    def test_delete_vending_machine(self, mock_input):
        # Setup
        mock_vending_machine_dao = MagicMock(spec=VendingMachineDAO)
        mock_product_dao = MagicMock(spec=ProductDAO)
        mock_seller_id = "test_seller_id"

        # Simula a função get_vending_machines_by_seller_id retornando uma lista de máquinas
        mock_vending_machine_dao.get_vending_machines_by_seller_id.return_value = [
            VendingMachine("TestMachine", "TestLocation", "test_seller_id")
        ]

        # Testa a função delete_vending_machine
        delete_vending_machine(mock_seller_id, None, mock_vending_machine_dao, mock_product_dao)

        # Verifica se o método delete_vending_machine foi chamado
        mock_vending_machine_dao.delete_vending_machine.assert_called_once()

        # Verifica se os produtos associados também foram deletados
        mock_product_dao.delete_products_by_vending_machine_id.assert_called_once()


if __name__ == "__main__":
    unittest.main()
