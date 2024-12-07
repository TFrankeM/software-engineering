import time
import sys
import os
import pandas as pd


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../database")))

from vending_machine_dao import VendingMachineDAO
from product_dao import ProductDAO


from view_vending_machine import view_vending_machines_basic_info 
from insert_vending_machine import insert_new_vending_machine 
from delete_vending_machine import delete_vending_machine 

def clear_console():
    """
        Console clearing function, (just works in Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    
def seller_actions(seller_id, db_pool):
    """
        Main flow for a seller to manage vending machines.
    
    Parameters:
        seller_id (str): The ID of the seller (owner of vending machines).
        db_connection (sqlite3.Connection): The database connection.
    """

    db_connection = db_pool.get_connection()         # Pega uma conexão do pool
    
    vending_machine_dao = VendingMachineDAO(db_connection)
    product_dao = ProductDAO(db_connection)

    # Check if the 'vending_machines' and 'products' tables exist and create them if necessary
    cursor = db_connection.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name IN ('vending_machines', 'products');
    """)
    
    existing_tables = [table[0] for table in cursor.fetchall()]
    
    if 'vending_machines' not in existing_tables:
        print("Creating the vending_machines table as it does not exist.")
        vending_machine_dao.create_table()
    
    if 'products' not in existing_tables:
        print("Creating the products table as it does not exist.")
        product_dao.create_table()

    while True:
        clear_console()

        print("\n", "~"*10, "Menu do vendedor", "~"*10, "\n")
        print("1. Ver lista de Vending Machines")
        print("2. Inserir nova Vending Machine")
        print("3. Apagar Vending Machine")
        print("0. Sair")
        action = input("Escolha uma ação: ")

        if action == "1":
            view_vending_machines_basic_info(seller_id, db_connection, vending_machine_dao, product_dao)
        elif action == "2":
            insert_new_vending_machine(seller_id, db_connection, vending_machine_dao)
        elif action == "3":
            delete_vending_machine(seller_id, db_connection, vending_machine_dao, product_dao)
        elif action == "0":
            break
        else:
            print("\rOpção inválida. Tente novamente.", flush=True)
            time.sleep(2)
    
    db_pool.release_connection(db_connection)        # Devolve a conexão ao pool
    