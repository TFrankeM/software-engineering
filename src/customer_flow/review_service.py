import pandas as pd
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../classes")))

from review import Review, ReviewFactory


def clear_console():
    """
    Console clearing function, (just works in Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')
def create_review(customer_id, db_connection, review_dao, vending_machine_dao, product_dao):
    """
    Function to interactively create a review for a product or vending machine.
    The user can cancel the review process at any point.

    Parameters:
    - customer_id (int): ID of the customer who is creating the review.
    - db_connection (sqlite3.Connection): The connection to the database.
    - review_dao (ReviewDAO): The data access object for interacting with the reviews table.
    - vending_machine_dao (VendingMachineDAO): Data access object to interact with vending machines.
    - product_dao (ProductDAO): Data access object to interact with products.
    """
    
    while True:
        clear_console()
        print("\n", "~"*10, "Faça uma Avaliação", "~"*10, "\n")

        print("1. Criar avaliação de produto")
        print("2. Criar avaliação de máquina")
        print("0. Voltar")

        option = input("Escolha uma opção: ")

        if option == "0":
            print("Voltando...")
            time.sleep(1)
            break
        
        review_type = None
        if option == "1":
            review_type = "product"
            break
        elif option == "2":
            review_type = "machine"
            break
        else:
            print("Opção inválida.")
            time.sleep(1)
            continue

    selected_product_id = None
    selected_machine_id = None
    while True:
        clear_console()
        if review_type == "product":
            product_name = input("Digite o nome do produto que deseja avaliar ou 'cancelar' para cancelar: ")

            if product_name == "cancelar":
                print("Operação cancelada.")
                time.sleep(1)
                return
            
            # Search for products with that name
            products = product_dao.get_products_by_name(product_name)

            if not products:
                print("Nenhum produto encontrado com esse nome. Tente novamente.")
                time.sleep(2)
                continue
            
            # Display the products found in a DataFrame
            product_data = {
                "Index": [],
                "Nome": [],
                "Descrição": [],
            }

            for index, product in enumerate(products, start=1):
                product_data["Index"].append(index)
                product_data["Nome"].append(product.name)
                product_data["Descrição"].append(product.description)

            df = pd.DataFrame(product_data)
            print(df.to_string(index=False))

            # Confirm selection
            selected_product = int(input("Digite o número do produto que deseja avaliar ou 0 para cancelar: "))

            if selected_product == 0 or selected_product > len(products):
                print("Operação cancelada.")
                time.sleep(2)
                return
            
            # Get selected product and save ID
            selected_product_id = products[selected_product - 1].id

            print("Opção selecionada.")
            time.sleep(1)

        elif review_type == "machine":
            clear_console()
            # Get Machine ID
            machine_name = input("Digite o nome da máquina de venda que deseja avaliar ou 'cancelar' para cancelar: ")
            
            if machine_name == "cancelar":
                print("Operação cancelada.")    # Sair da tela de avaliação
                time.sleep(1)
                return
            
            # Search for machines with that name
            machines = vending_machine_dao.get_vending_machines_by_name(machine_name)

            if not machines:
                print("Nenhuma máquina encontrada com esse nome. Tente novamente.")
                time.sleep(2)
                continue
            
            # Display the machines found in a DataFrame
            machine_data = {
                "Index": [],
                "Nome": [],
                "Localização": []
            }

            for index, machine in enumerate(machines, start=1):
                machine_data["Index"].append(index)
                machine_data["Nome"].append(machine.name)
                machine_data["Localização"].append(machine.location)

            df = pd.DataFrame(machine_data)
            print(df.to_string(index=False))

            # Confirm selection
            selected_machine = int(input("Digite o número da máquina que deseja avaliar ou 0 para cancelar: "))

            if selected_machine == 0 or selected_machine > len(machines):
                print("Operação cancelada.")    # Sair da tela de avaliação
                time.sleep(2)
                return

            # Get the selected machine and save the ID
            selected_machine_id = machines[selected_machine - 1].id

        print("Opção selecionada.")
        time.sleep(1)

        # Get user rating
        while True:
            clear_console()
            try:
                rating = int(input("Dê uma nota de 0 a 5 para sua avaliação: "))
                if rating < 0 or rating > 5:
                    raise ValueError("Nota deve estar entre 0 e 5.")
                time.sleep(1)
                break
            except ValueError:
                print("Nota inválida. Deve ser um número entre 0 e 5.")
                time.sleep(2)
                return

        while True:
            clear_console()
            # Get comment (optional)
            comment = input("Agora, deixe um comentário (opcional, pressione Enter para pular): ")
            if len(comment) > Review.MAX_COMMENT_LENGTH:
                print(f"Comentário muito longo. Deve ter no máximo {Review.MAX_COMMENT_LENGTH} caracteres.")
                time.sleep(2.5)
            else:
                break
        
        # Create the review using the ReviewFactory
        try:
            review = ReviewFactory.create_review(
                review_type,
                customer_id,
                rating,
                comment,
                product_id=selected_product_id,
                machine_id=selected_machine_id
            )
            #Insert the review into the database
            review_dao.insert_review(review)
            print("\n==> Sua avaliação foi registrada com sucesso!")
            time.sleep(2)
            return
        except ValueError as e:
            print(f"Erro ao criar avaliação: {e}")

        time.sleep(2)

