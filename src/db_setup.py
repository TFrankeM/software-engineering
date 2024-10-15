import sqlite3


def create_database():
    """
    Creates the main database and all the necessary tables.
    """
    conn = sqlite3.connect("vending_system.db")

    #implemente aqui a lógica de criação do banco de dados 'vending_machine.db'.

if __name__ == "__main__":
    create_database()
