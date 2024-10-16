import time
import sys
import os
import pandas as pd


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/classes")))

from vending_machine import VendingMachine
from product import Product

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/database")))

from vending_machine_dao import VendingMachineDAO
from product_dao import ProductDAO


def clear_console():
    """
    Console clearing function, (just works in Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def view_vending_machine_details(vending_machine, db_connection, vending_machine_dao):
    """
    Display details of the selected vending machine, including products and stock.

    Parameters:
        vending_machine (VendingMachine): The selected vending machine object.
        db_connection (sqlite3.Connection): The database connection.
    """
    product_dao = ProductDAO(db_connection)

    print(f"\nDetalhes da Máquina: {vending_machine.name}")
    print(f"Localização: {vending_machine.location}")
    
    # Retrieve all products for this vending machine
    products = product_dao.get_products_by_vending_machine_id(vending_machine.id)

    if not products:
        print("  Não há produtos cadastrados nesta máquina.")
    else:
        print("  Produtos e estoque disponíveis:")
        for product in products:
            print(f"    - Produto: {product[1]}, Quantidade: {product[4]}")  # product[1] -> name, product[4] -> quantity

            
def view_vending_machines_basic_info(seller_id, db_connection, vending_machine_dao):
    """
    List all vending machines owned by the seller and display basic info.

    Parameters:
        seller_id (str): The ID of the seller.
        db_connection (sqlite3.Connection): The database connection.
        vending_machine_dao: sql table.
    """
    

    # Fetch all vending machines owned by this seller
    vending_machines = vending_machine_dao.get_vending_machines_by_seller_id(seller_id)

    if not vending_machines:
        clear_console()
        print("\n", "~"*10, "Visualize suas máquinas de venda!", "~"*10, "\n")

        print("\nVocê não possui máquinas de venda cadastradas.")
        print("Tente inserir uma primeiro.")
        time.sleep(2)
        return
    
        # Organize the data into a DataFrame
    vending_machines_data = {
        "Index": [],
        "Nome": [],
        "Localização": []
    }
    
    for index, vm in enumerate(vending_machines, start=1):
        vending_machines_data["Index"].append(index)
        vending_machines_data["Nome"].append(vm.name)
        vending_machines_data["Localização"].append(vm.location)

    while True:
        try:
            clear_console()
            print("\n", "~"*10, "Visualize suas máquinas de venda!", "~"*10, "\n")

            # Create and print the DataFrame
            df = pd.DataFrame(vending_machines_data)
            print(df.to_string(index=False))  # Display the table without pandas' automatic index
            
            print("\n==> Digite 0 para cancelar a operação e voltar ao menu anterior.\n")
            selected_machine = int(input("Digite o número da máquina que deseja ver os detalhes: "))

            if selected_machine == 0:
                print("Operação cancelada. Retornando ao menu.")
                time.sleep(1)
                return

            elif 0 < selected_machine <= len(vending_machines):
                # Exibe os detalhes da máquina selecionada
                view_vending_machine_details(vending_machines[selected_machine - 1], db_connection, vending_machine_dao)
                break
            else:
                print("Número inválido. Escolha uma opção válida.")
                time.sleep(1)

        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")
            time.sleep(1)


def insert_new_vending_machine(seller_id, db_connection, vending_machine_dao):
    """
    Insert a new vending machine for the seller.

    Parameters:
        seller_id (str): The ID of the seller.
        db_connection (sqlite3.Connection): The database connection.
    """
    clear_console()
    print("\n", "~"*10, "Insira nova máquina de venda", "~"*10, "\n")

    print("\n==> A qualquer momento, digite 0 para cancelar a operação e voltar ao menu anterior.\n")
    
    # Get the name of the new vending machine
    name = input("Digite o nome da nova máquina de venda: ")
    if name == "0":
        print("Operação cancelada.")
        time.sleep(0.5)
        return
    
    # Get the location of the new vending machine
    location = input("Digite a localização da nova máquina de venda: ")
    if location == "0":
        print("Operação cancelada.")
        time.sleep(0.5)
        return
    
    new_vending_machine = VendingMachine(name=name, location=location, owner_id = seller_id)
    print("Id logo após a criação da instância da classe VendingMachine: ", new_vending_machine.id)
    # Insert the new vending machine into the database
    vending_machine_dao.insert_vending_machine(new_vending_machine)
    print(f"\nMáquina de venda '{name}' foi inserida com sucesso.")
    time.sleep(2)


def delete_vending_machine(seller_id, db_connection, vending_machine_dao):
    """
    Delete a vending machine owned by the seller.

    Parameters:
        seller_id (str): The ID of the seller.
        db_connection (sqlite3.Connection): The database connection.
    """
    # Fetch all vending machines owned by this seller
    vending_machines = vending_machine_dao.get_vending_machines_by_seller_id(seller_id)

    if not vending_machines:
        clear_console()
        print("\n", "~"*10, "Delete uma máquina de venda", "~"*10, "\n")
        print("\nVocê não possui máquinas de venda cadastradas.")
        print("Tente inserir uma máquina primeiro.")
        time.sleep(2)
        return    
    
    while True:
        try:
            clear_console()
            print("\n", "~"*10, "Delete uma máquina de venda", "~"*10, "\n")

            print("\nLista de Vending Machines para deletar:")
            for index, vm in enumerate(vending_machines, start=1):
                print(f"{index}. Nome: {vm.name}, Localização: {vm.location}")

            print("\n==> Digite 0 para cancelar a operação e voltar ao menu anterior.")
            selected_machine = int(input("Digite o número da máquina que deseja deletar: "))

            if selected_machine == 0:
                print("Operação cancelada.")
                time.sleep(0.5)
                return
            
            elif 0 < selected_machine <= len(vending_machines):
                # Converter o UUID para string antes de passar para o banco de dados
                vending_machine_dao.delete_vending_machine(str(vending_machines[selected_machine - 1].id))
                #print('Id da máquina que queremos deletar:', str(vending_machines[selected_machine - 1].id))
                print(f"Máquina '{vending_machines[selected_machine - 1].name}' foi deletada com sucesso.")
                time.sleep(2)
                break

            else:
                print("Número inválido. Escolha uma opção válida.")
                time.sleep(1)
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")
            time.sleep(1)


def seller_actions(seller_id, db_connection):
    """
    Main flow for a seller to manage vending machines.
    
    Parameters:
        seller_id (str): The ID of the seller (owner of vending machines).
        db_connection (sqlite3.Connection): The database connection.
    """
    
    vending_machine_dao = VendingMachineDAO(db_connection)

    # Check if the 'vending_machines' table exists and create it if necessary
    cursor = db_connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='vending_machines';")
    table_exists = cursor.fetchone()

    if not table_exists:
        print("Creating the vending_machines table as it does not exist.")
        vending_machine_dao.create_table()

    while True:
        clear_console()

        print("\n", "~"*10, "Menu do vendedor", "~"*10)
        print("1. Ver lista de Vending Machines")
        print("2. Inserir nova Vending Machine")
        print("3. Apagar Vending Machine")
        print("4. Sair")
        action = input("Escolha uma ação: ")

        if action == "1":
            view_vending_machines_basic_info(seller_id, db_connection, vending_machine_dao)
        elif action == "2":
            insert_new_vending_machine(seller_id, db_connection, vending_machine_dao)
        elif action == "3":
            delete_vending_machine(seller_id, db_connection, vending_machine_dao)
        elif action == "4":
            print("Saindo...")
            break
        else:
            print("\rOpção inválida. Tente novamente.", flush=True)
            time.sleep(2)
            return seller_actions(seller_id, db_connection)

