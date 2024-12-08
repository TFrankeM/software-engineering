import time
import sys
import os
import pandas as pd


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../classes")))

from vending_machine import VendingMachine

def clear_console():
    """
        Console clearing function, (just works in Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def insert_new_vending_machine(seller_id, db_connection, vending_machine_dao):
    """
        Insert a new vending machine for the seller.

    Parameters:
        seller_id (str): The ID of the seller.
        db_connection (sqlite3.Connection): The database connection.
        vending_machine_dao (VendingMachineDAO): Data access object for interacting with vending machine in the database.
    """
    clear_console()
    print("\n", "~"*10, "Insira nova máquina de venda", "~"*10, "\n")

    print("\n==> A qualquer momento, digite 0 para cancelar a operação e voltar ao menu anterior.\n")
    
    # Get the name of the new vending machine
    name = input("Digite o nome da nova máquina de venda: ")
    if name == "0":
        return
    
    # Get the location of the new vending machine
    location = input("Digite a localização da nova máquina de venda: ")
    if location == "0":
        return
    
    new_vending_machine = VendingMachine(name=name, location=location, owner_id = seller_id)
    #print("Id logo após a criação da instância da classe VendingMachine: ", new_vending_machine.id)
    # Insert the new vending machine into the database
    vending_machine_dao.insert_vending_machine(new_vending_machine)
    print(f"\nMáquina de venda '{name}' foi inserida com sucesso.")
    
    input("\n==> Pressione Enter para voltar ao menu.")