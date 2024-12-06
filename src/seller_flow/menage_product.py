import time
import sys
import os
import pandas as pd


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../classes")))

from vending_machine import VendingMachine
from product import Product

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../database")))

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