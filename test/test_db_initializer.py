import unittest
import sqlite3
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from db_initializer import DBConnectionPool

class TestDBConnectionPool(unittest.TestCase):
    def setUp(self):
        """
        Setup method to initialize the test environment.
        This method is called before each test case.
        """
        self.db_name = ":memory:"  # Usar um banco de dados em memória para testes
        self.max_connections = 3
        self.pool = DBConnectionPool(self.db_name, self.max_connections)

    def test_initialization(self):
        """
        Test the initialization of the connection pool.
        Ensure that the pool is correctly initialized with the given number of connections.
        """
        self.assertEqual(self.pool.max_connections, self.max_connections)
        self.assertEqual(self.pool.pool.qsize(), self.max_connections)
        self.assertEqual(self.pool.db_name, self.db_name)

    def test_get_connection(self):
        """
        Test getting a connection from the pool.
        Ensure that the connection is correctly retrieved from the pool.
        """
        connection = self.pool.get_connection()
        self.assertIsInstance(connection, sqlite3.Connection)
        self.assertEqual(self.pool.pool.qsize(), self.max_connections - 1)
        
        # Release the connection to restore the pool to its full size
        self.pool.release_connection(connection)

    def test_release_connection(self):
        """
        Test releasing a connection back to the pool.
        Ensure that the connection is correctly returned to the pool.
        """
        connection = self.pool.get_connection()
        self.pool.release_connection(connection)
        self.assertEqual(self.pool.pool.qsize(), self.max_connections)

    def test_close_all_connections(self):
        """
        Test closing all connections in the pool.
        Ensure that all connections are closed and the pool is empty.
        """
        self.pool.close_all_connections()
        self.assertTrue(self.pool.pool.empty())

    def tearDown(self):
        """
        Teardown method to clean up after each test case.
        This method is called after each test case.
        """
        self.pool.close_all_connections()

if __name__ == "__main__":
    unittest.main()
