import threading
import sqlite3
import queue

class DBConnectionPool:
    def __init__(self, db_name, max_connections=1):
        """
        Pool of connections to the database.

        :param db_name: Database name.
        :param max_connections: Maximum number of simultaneous connections allowed.
        """
        self.db_name = db_name
        self.max_connections = max_connections
        self.pool = queue.Queue(max_connections)
        
        # Inicializa o pool com as conexões
        for _ in range(max_connections):
            connection = sqlite3.connect(db_name)
            self.pool.put(connection)
        
        self.lock = threading.Lock()

    def get_connection(self):
        """
        Gets a connection from the pool. If no connections are available, waits until one becomes available.
        """
        with self.lock:
            return self.pool.get()

    def release_connection(self, connection):
        """
        Releases a connection back to the pool.
        """
        with self.lock:
            self.pool.put(connection)

    def close_all_connections(self):
        """
        Closes all connections in the pool.
        """
        while not self.pool.empty():
            connection = self.pool.get()
            connection.close()


def initialize_db():
    """
    Initializes the database connection pool.

    :return: Connection pool instance.
    """
    db_name = "vending_system.db"

    max_connections = 5  # No futuro, quando expandirmos a aplicação, o valor pode ser escalado

    return DBConnectionPool(db_name, max_connections)
