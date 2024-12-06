import time
import sys
import os
import pandas as pd


def clear_console():
    """
        Console clearing function, (just works in Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def delete_vending_machine(seller_id, db_connection, vending_machine_dao, product_dao):
    """
        Delete a vending machine owned by the seller and all associated products.

    Parameters:
        seller_id (str): The ID of the seller.
        db_connection (sqlite3.Connection): The database connection.
        vending_machine_dao (VendingMachineDAO): Data access object for interacting with vending machines in the database.
        product_dao (ProductDAO): Data access object for interacting with products in the database.
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
    # Create the DataFrame
    df = pd.DataFrame(vending_machines_data)

    while True:
        try:
            clear_console()
            print("\n", "~"*10, "Delete uma máquina de venda", "~"*10, "\n")

            print("\nLista de Vending Machines para deletar:")
            
            print(df.to_string(index=False))  # Display the table without pandas' automatic index
            
            print("\n==> Digite 0 para cancelar a operação e voltar ao menu anterior.")
            selected_machine = int(input("Digite o número da máquina que deseja deletar: "))

            if selected_machine == 0:
                print("Operação cancelada.")
                time.sleep(0.5)
                return
            
            elif 0 < selected_machine <= len(vending_machines):
                selected_machine_id = str(vending_machines[selected_machine - 1].id)
                selected_machine_name = vending_machines[selected_machine - 1].name

                #deletar os produtos associados à máquina
                product_dao.delete_products_by_vending_machine_id(selected_machine_id)

                # Deletar a máquina de venda
                vending_machine_dao.delete_vending_machine(selected_machine_id)

                #print('Id da máquina que quero deletar:', str(vending_machines[selected_machine - 1].id))
                print(f"Máquina '{selected_machine_name}' foi deletada com sucesso.")
                time.sleep(2)
                break

            else:
                print("Número inválido. Escolha uma opção válida.")
                time.sleep(1)

        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")
            time.sleep(1)