import time
import sys
import os
import pandas as pd

from menage_product import create_new_product, remove_product, update_product


def clear_console():
    """
        Console clearing function, (just works in Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def view_vending_machine_details(vending_machine, db_connection, product_dao):
    """
        Display details of the selected vending machine, including products and stock.

    Parameters:
        vending_machine (VendingMachine): The selected vending machine object.
        db_connection (sqlite3.Connection): The database connection.
        product_dao (ProductDAO): Data access object for interacting with products in the database.
    """

    while True:
        try:
            clear_console()
            print("\n", "~"*10, "Visualize detalhes da sua máquina de vendas", "~"*10, "\n")

            print(f"\nDetalhes da Máquina: {vending_machine.name}")
            print(f"Localização: {vending_machine.location}\n")

            print(f"Avaliação Média: {vending_machine.average_rating}\n")


            # Retrieve all products for this vending machine
            products = product_dao.get_products_by_vending_machine_id(vending_machine.id)

            if not products:
                print(">>> Não há produtos cadastrados nesta máquina. <<<")
                
            else:
                # Organize the product data into a DataFrame
                product_data = {
                    "Produto": [product.name for product in products],
                    "Quantidade": [product.quantity for product in products],
                    "Preço": [product.price for product in products],
                    "Descrição": [product.description for product in products],
                    "Avaliação Média": [product.average_rating for product in products]
                }
                df = pd.DataFrame(product_data)
                df.index = df.index + 1 #Set the index to start at 1
                print(df.to_string())

            # Menu options for managing products
            print("\n==> Selecione uma ação:")
            print("1. Adicionar novo produto")
            print("2. Remover um produto")
            print("3. Atualizar informações de um produto")
            print("0. Voltar ao menu anterior")

            action = input("\nDigite o número da ação desejada: ")

            if action == "1":
                create_new_product(vending_machine, product_dao)

            elif action == "2":
                remove_product(df, products, vending_machine, product_dao)

            elif action == "3":
                update_product(df, products, vending_machine, product_dao)

            elif action == "0":
                break  # Sai do loop e volta ao menu anterior

            else:
                print("Número inválido. Escolha uma opção válida.")
                time.sleep(1)

        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")
            time.sleep(1)


def view_vending_machines_basic_info(seller_id, db_connection, vending_machine_dao, product_dao):
    """
        List all vending machines owned by the seller and display basic info.

    Parameters:
        seller_id (str): The ID of the seller.
        db_connection (sqlite3.Connection): The database connection.
        vending_machine_dao (VendingMachineDAO): Data access object for interacting with vending machine in the database.
        product_dao (ProductDAO): Data access object for interacting with products in the database.
    """

    # Fetch all vending machines owned by this seller
    vending_machines = vending_machine_dao.get_vending_machines_by_seller_id(seller_id)

    if not vending_machines:
        clear_console()
        print("\n", "~"*10, "Visualize suas máquinas de venda!", "~"*10, "\n")

        print("\n>>> Você não possui máquinas de venda cadastradas. <<<")
        print("Tente inserir uma primeiro.")

        input("\n==> Pressione Enter para voltar ao menu.")
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
            print("\n", "~"*10, "Visualize suas máquinas de venda!", "~"*10, "\n")
            
            print(df.to_string(index=False))  # Display the table without pandas' automatic index
            
            print("\n==> Digite 0 para cancelar a operação e voltar ao menu anterior.\n")
            selected_machine = int(input("Digite o número da máquina que deseja ver os detalhes: "))

            if selected_machine == 0:
                return

            elif 0 < selected_machine <= len(vending_machines):
                # Exibe os detalhes da máquina selecionada
                view_vending_machine_details(vending_machines[selected_machine - 1], db_connection, product_dao)
                break
            else:
                print("Número inválido. Escolha uma opção válida.")
                time.sleep(1)

        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")
            time.sleep(1)