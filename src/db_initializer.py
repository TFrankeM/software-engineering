import sqlite3

def initialize_db():
    """
    Function to initialize the connection to the database 'vending_system.db'.

    Returns:
        connection (sqlite3.Connection): The active connection to the database.
    """
    # Connect to the database or create the database file if it does not exist
    db_name = "vending_system.db"
    connection = sqlite3.connect(db_name)
    
    return connection
