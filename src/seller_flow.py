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
from seller_dao import SellerDAO
from user import UserFactory


def clear_console():
    """
        Console clearing function, (just works in Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def create_new_product(vending_machine, product_dao):
    """
        Create and add a new product to the selected vending machine.
    
    Parameters:
        vending_machine (VendingMachine): The selected vending machine object.
        product_dao (ProductDAO): Data access object for interacting with products in the database.
    """
    clear_console()
    print("\n", "~"*10, "Adicionar novo produto à máquina", "~"*10, "\n")

    name = input("Digite o nome do produto: ")
    description = input("Digite a descrição do produto: ")

    try:
        price = float(input("Digite o preço do produto: "))
        quantity = int(input("Digite a quantidade do produto: "))
    except ValueError:
        print("Entrada inválida. Certifique-se de inserir valores numéricos para preço e quantidade.")
        time.sleep(2)
        return

    confirm = input("Você realmente deseja adicionar esse produto?: [responda com 's' ou 'n'] ").strip()
    
    if confirm == "s":
        new_product = Product(name=name, description=description, price=price, quantity=quantity, machine_id=str(vending_machine.id))
        
        product_dao.insert_product(new_product)
        print(f"Produto '{name}' foi adicionado com sucesso!")
        time.sleep(2)
    
    elif confirm == "n":
        print(f"Operação cancelada.")
        time.sleep(2)
    
    else:
        print(f"Entrada inválida. Operação cancelada.")
        time.sleep(2)


def remove_product(df, products, vending_machine, product_dao):
    """
        Remove a product from the selected vending machine.
    
    Parameters:
        df (pd.DataFrame): Dataframe with products data.
        products (list): List of Product objects.
        vending_machine (VendingMachine): The selected vending machine object.
        product_dao (ProductDAO): Data access object for interacting with products in the database.
    """

    # Verifica se o DataFrame está vazio
    if df.empty:
        clear_console()
        print("\n", "~"*10, "Remover produto", "~"*10, "\n")

        print(f"Detalhes da Máquina: {vending_machine.name}")
        print(f"Localização: {vending_machine.location}\n")
        
        print(f"\n>>> Não há produtos para remover nesta máquina. <<<")
        time.sleep(4)

        return

    while True:
        try:
            clear_console()
            print("\n", "~"*10, "Remover produto", "~"*10, "\n")

            print(f"Detalhes da Máquina: {vending_machine.name}")
            print(f"Localização: {vending_machine.location}\n")

            # Exibe o DataFrame para o usuário
            print(df.to_string())

            selected_product = int(input("\nDigite o número do produto que deseja remover ou 0 para voltar: "))

            if selected_product == 0:
                return

            if 0 < selected_product <= len(df):
                product_id = products[selected_product - 1].id
                product_name = products[selected_product - 1].name

                # Remove o produto do banco de dados
                product_dao.delete_product(product_id)
                print(f"\n==> Produto '{product_name}' foi removido com sucesso.")

                time.sleep(2)
                break

            else:
                print("Número inválido. Escolha uma opção válida.")
                time.sleep(1)

        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")
            time.sleep(3)


def update_product(df, products, vending_machine, product_dao):
    """
        Update product information for a selected product in the vending machine.
    
    Parameters:
        df (pd.DataFrame): Dataframe with products data.
        products (list): List of Product objects.
        vending_machine (VendingMachine): The selected vending machine object.
        product_dao (ProductDAO): Data access object for interacting with products in the database.
    """

    if df.empty:
        clear_console()
        print("\n", "~"*10, "Atualizar informações de um produto", "~"*10, "\n")

        print(f"Detalhes da Máquina: {vending_machine.name}")
        print(f"Localização: {vending_machine.location}\n")

        print("\n>>> Não há produtos cadastrados nesta máquina. <<<")
        time.sleep(4)
        return

    while True:
        try:
            clear_console()
            print("\n", "~"*10, "Atualizar informações de um produto", "~"*10, "\n")

            print(f"Detalhes da Máquina: {vending_machine.name}")
            print(f"Localização: {vending_machine.location}\n")

            # Exibe o DataFrame para o usuário
            print(df.to_string())

            selected_product = int(input("\nDigite o número do produto que deseja atualizar ou 0 para voltar: "))

            if selected_product == 0:
                return

            if 0 < selected_product <= len(df):
                product = products[selected_product - 1]

                ##Sslicita as novas informações do produto, mantendo os valores atuais se o usuário pressionar Enter
                new_name = input(f"Digite o novo nome para '{product.name}' ou pressione Enter para manter o mesmo: ") or product.name
                new_description = input(f"Digite a nova descrição ou pressione Enter para manter a mesma: ") or product.description
                new_price = input(f"Digite o novo preço [{product.price}] ou pressione Enter para manter o mesmo: ")
                new_quantity = input(f"Digite a nova quantidade [{product.quantity}] ou pressione Enter para manter a mesma: ")

                # Valida entradas numéricas
                new_price = float(new_price) if new_price else product.price
                new_quantity = int(new_quantity) if new_quantity else product.quantity

                confirm = input("Você realmente deseja adicionar esse produto?: [responda com 's' ou 'n'] ").strip()
    
                if confirm == "s":
                    updated_product = Product(
                        name=new_name, 
                        description=new_description, 
                        price=new_price, 
                        quantity=new_quantity, 
                        machine_id=str(vending_machine.id)
                    )
                    updated_product.id = product.id
                    product_dao.update_product(updated_product)

                    print(f"\n==> Produto '{new_name}' foi atualizado com sucesso!")
                    time.sleep(2)
                    break
                elif confirm == "n":
                    print("Operação cancelada.")
                    time.sleep(2)
                    break
                else:
                    print("Entrada inválida. Operação cancelada.")
                    time.sleep(2)
                    break

            else:
                print("Número inválido. Escolha uma opção válida.")
                time.sleep(1)

        except ValueError:
            print("Entrada inválida. Por favor, insira um número válido.")
            time.sleep(1)


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
                    "Descrição": [product.description for product in products]
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
                print("Voltando ao menu anterior...")
                time.sleep(1)
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

        print("\nVocê não possui máquinas de venda cadastradas.")
        print("Tente inserir uma primeiro.")

        time.sleep(4)
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
                print("Operação cancelada. Retornando ao menu.")
                time.sleep(1)
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
    #print("Id logo após a criação da instância da classe VendingMachine: ", new_vending_machine.id)
    # Insert the new vending machine into the database
    vending_machine_dao.insert_vending_machine(new_vending_machine)
    print(f"\nMáquina de venda '{name}' foi inserida com sucesso.")
    time.sleep(2)


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


def seller_actions(seller_id, db_connection):
    """
        Main flow for a seller to manage vending machines.
    
    Parameters:
        seller_id (str): The ID of the seller (owner of vending machines).
        db_connection (sqlite3.Connection): The database connection.
    """
    
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

        print("\n", "~"*10, "Menu do vendedor", "~"*10)
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
            print("Saindo...")
            break
        else:
            print("\rOpção inválida. Tente novamente.", flush=True)
            time.sleep(2)
            return seller_actions(seller_id, db_connection)


def create_seller_account(db_connection):
    """
    Create a new seller account and insert it into the database.

    Parameters:
        db_connection (sqlite3.Connection): The database connection.
    """
    print("Criar Conta de Vendedor:")
    name = input("Nome: ")
    email = input("Email: ")
    password = input("Senha: ")
    address = input("Endereço: ")
    
    # Cria um novo objeto Seller
    seller = UserFactory(user_type="Seller",name=name, email=email, password=password, address=address)
    
    # Insere o novo vendedor no banco de dados
    seller_dao = SellerDAO(db_connection)
    # Check if the 'sellers' table exists and create it if necessary
    cursor = db_connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sellers';")
    table_exists = cursor.fetchone()

    if not table_exists:
        print("Creating the seller table as it does not exist.")
        seller_dao.create_table()
    
    seller_dao.insert_seller(seller)
    
    print("Conta de vendedor criada com sucesso!")
    #para verificar se o vendedor foi inserido corretamente e inserido na tabela sellers
    """
    cursor.execute("SELECT * FROM sellers")
    print(cursor.fetchall())
    """

    

