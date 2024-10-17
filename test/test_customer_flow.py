from unittest.mock import patch
import unittest
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from customer_flow import customer_actions

import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from customer_flow import (
    customer_actions, 
    create_problem_report, 
    create_review, 
    view_vending_machines_for_customer, 
    view_vending_machine_reviews,
    create_customer_account
)
from review import Review
from review_dao import ReviewDAO
from vending_machine_dao import VendingMachineDAO
from product_dao import ProductDAO
from problem_report_dao import ProblemReportDAO
from customer_dao import CustomerDAO
from customer import Customer

class TestCustomerFlow(unittest.TestCase):
    def setUp(self):
        # Simulate a SQLite connection for all tests
        self.db_connection = MagicMock(spec=sqlite3.Connection)
        self.customer_id = "test_customer_id"


    @patch("builtins.input", side_effect=["m", "1", "0", "Comentário"])
    def test_create_problem_report_machine(self, mock_input):
        # Setup mock DAOs
        mock_problem_report_dao = MagicMock(spec=ProblemReportDAO)

        with patch("customer_flow.ProblemReportDAO", return_value=mock_problem_report_dao):
            create_problem_report(self.customer_id, self.db_connection)

            # Verify the insert was called
            self.assertTrue(mock_problem_report_dao.insert_problem_report.called)


    @patch("builtins.input", side_effect=["s", "2", "Comentário"])
    def test_create_problem_report_system(self, mock_input):
        # Setup mock DAOs
        mock_problem_report_dao = MagicMock(spec=ProblemReportDAO)

        with patch("customer_flow.ProblemReportDAO", return_value=mock_problem_report_dao):
            create_problem_report(self.customer_id, self.db_connection)

            # Verify the insert was called
            self.assertTrue(mock_problem_report_dao.insert_problem_report.called)


    @patch("builtins.input", side_effect=["1", "1", "0"])
    def test_view_vending_machines_for_customer(self, mock_input):
        # Setup mock DAOs
        mock_vending_machine_dao = MagicMock(spec=VendingMachineDAO)
        mock_vending_machine = MagicMock()
        mock_vending_machine.id = "test_machine_id"
        mock_vending_machine_dao.get_all_vending_machines.return_value = [mock_vending_machine]

        with patch("customer_flow.VendingMachineDAO", return_value=mock_vending_machine_dao):
            view_vending_machines_for_customer(self.db_connection)

            # Verify that the vending machine list was retrieved
            mock_vending_machine_dao.get_all_vending_machines.assert_called_once()


    @patch("builtins.input", side_effect=["Nome", "email@test.com", "senha123", "Endereço", "sim"])
    def test_create_customer_account(self, mock_input):
        # Setup mock DAOs
        mock_customer_dao = MagicMock(spec=CustomerDAO)

        with patch("customer_flow.CustomerDAO", return_value=mock_customer_dao):
            create_customer_account(self.db_connection)

            # Verify that the customer account was created
            mock_customer_dao.insert_customer.assert_called_once()


if __name__ == "__main__":
    unittest.main()
