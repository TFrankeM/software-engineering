from abc import ABC, abstractmethod
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


class ReviewStrategy(ABC):
    """
    Strategy interface for collecting data to create a review.
    """
    
    @abstractmethod
    def collect_data(self, customer_id, db_connection, product_dao, vending_machine_dao):
        pass


class ProductReviewStrategy(ReviewStrategy):
    """
    Strategy for creating a product review.
    """
    
    def collect_data(self, customer_id, db_connection, product_dao, vending_machine_dao):
        selected_product_id = None
        
        while True:
            clear_console()
            product_name = input("Digite o nome do produto que deseja avaliar ou 'cancelar' para cancelar: ")

            if product_name == "cancelar":
                print("Operação cancelada.")
                time.sleep(1)
                return None

            # Buscar produtos com o nome fornecido
            products = product_dao.get_products_by_name(product_name)

            if not products:
                print("Nenhum produto encontrado com esse nome. Tente novamente.")
                time.sleep(2)
                continue

            # Exibir produtos encontrados
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

            # Confirmar seleção
            selected_product = int(input("Digite o número do produto que deseja avaliar ou 0 para cancelar: "))

            if selected_product == 0 or selected_product > len(products):
                print("Operação cancelada.")
                time.sleep(2)
                return None

            # Selecionar o produto e salvar o ID
            selected_product_id = products[selected_product - 1].id
            break
        
        return selected_product_id


class MachineReviewStrategy(ReviewStrategy):
    """
    Strategy for creating a vending machine review.
    """
    
    def collect_data(self, customer_id, db_connection, product_dao, vending_machine_dao):
        selected_machine_id = None
        
        while True:
            clear_console()
            machine_name = input("Digite o nome da máquina de venda que deseja avaliar ou 'cancelar' para cancelar: ")

            if machine_name == "cancelar":
                print("Operação cancelada.")
                time.sleep(1)
                return None

            # Buscar máquinas com o nome fornecido
            machines = vending_machine_dao.get_vending_machines_by_name(machine_name)

            if not machines:
                print("Nenhuma máquina encontrada com esse nome. Tente novamente.")
                time.sleep(2)
                continue

            # Exibir máquinas encontradas
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

            # Confirmar seleção
            selected_machine = int(input("Digite o número da máquina que deseja avaliar ou 0 para cancelar: "))

            if selected_machine == 0 or selected_machine > len(machines):
                print("Operação cancelada.")
                time.sleep(2)
                return None

            # Selecionar a máquina e salvar o ID
            selected_machine_id = machines[selected_machine - 1].id
            break
        
        return selected_machine_id


def create_review(customer_id, db_connection, review_dao, vending_machine_dao, product_dao):
    """
    Function to create a product or machine evaluation.
    Interacts with the user to determine the type of evaluation and calls the appropriate strategy.

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

        option = input("\n==> Escolha uma opção: ")

        if option == "0":
            print("Voltando...")
            time.sleep(0.5)
            return
        
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
    
    # Seleciona a estratégia apropriada com base no tipo de avaliação
    if review_type == "product":
        review_strategy = ProductReviewStrategy()
    elif review_type == "machine":
        review_strategy = MachineReviewStrategy()

    # Coleta os dados necessários para a avaliação usando a estratégia
    selected_item_id = review_strategy.collect_data(
        customer_id, db_connection, product_dao, vending_machine_dao
    )

    if selected_item_id is None:
        return  # Se o processo foi cancelado ou houve erro na seleção

    # Solicita a nota de avaliação
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

    # Comentário opcional
    while True:
        clear_console()
        comment = input("Agora, deixe um comentário (opcional, pressione Enter para pular): ")
        if len(comment) > Review.MAX_COMMENT_LENGTH:
            print(f"Comentário muito longo. Deve ter no máximo {Review.MAX_COMMENT_LENGTH} caracteres.")
            time.sleep(2.5)
        else:
            break

    # Criação da avaliação usando a ReviewFactory
    try:
        review = ReviewFactory.create_review(
            review_type,
            customer_id,
            rating,
            comment,
            product_id=selected_item_id if review_type == "product" else None,
            machine_id=selected_item_id if review_type == "machine" else None
        )
        # Insere a avaliação no banco de dados
        review_dao.insert_review(review)

        # Atualizar a avaliação média do produto ou da máquina
        if review_type == "product":
            # Calcula a média de avaliações do produto
            avg_rating = review_dao.calculate_average_rating_for_product(selected_item_id)
            # Atualiza a avaliação média do produto no banco de dados
            product_dao.update_product_average_rating(selected_item_id, avg_rating)
        elif review_type == "machine":
            # Calcula a média de avaliações da máquina
            avg_rating = review_dao.calculate_average_rating_for_machine(selected_item_id)
            # Atualiza a avaliação média da máquina no banco de dados
            vending_machine_dao.update_machine_average_rating(selected_item_id, avg_rating)

        print("\n==> Sua avaliação foi registrada com sucesso!") 

        input("\nPressione qualquer tecla para voltar.")
        return

    except ValueError as e:
        print(f"Erro ao criar avaliação: {e}")
        time.sleep(2)

