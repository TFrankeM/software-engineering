import pandas as pd
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/database")))

from vending_machine_dao import VendingMachineDAO
from product_dao import ProductDAO
from problem_report_dao import ProblemReportDAO
from problem_report import ProblemReport
from review_dao import ReviewDAO
from review import Review
from problem_types import SYSTEM_PROBLEM_TYPES, MACHINE_PROBLEM_TYPES
from customer_dao import CustomerDAO
from user import UserFactory

def clear_console():
    """
    Console clearing function, (just works in Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def create_problem_report(customer_id, db_connection):
    """
    Create a problem report for a vending machine or the system.
    """
    clear_console()
    print("~"*10, "Reportar Problema", "~"*10)

    # Pergunta se o problema é relacionado a uma máquina ou ao sistema
    tipo_problema = input("\nO problema está relacionado a uma máquina ou ao sistema? (Digite 'm' para máquina ou 's' para sistema): ").strip().lower()
    
    # Se for um problema de máquina
    if tipo_problema == 'm':
        machine_id = input("Digite o ID da máquina com problema: ")
        print("Selecione o tipo de problema de máquina:")
        for idx, problem in enumerate(MACHINE_PROBLEM_TYPES, 1):
            print(f"{idx}. {problem}")
        problem_choice = int(input("Digite o número do tipo de problema: "))
        problem_type = MACHINE_PROBLEM_TYPES[problem_choice - 1]

    # Se for um problema do sistema
    elif tipo_problema == 's':
        machine_id = None  # O problema de sistema não está associado a uma máquina
        print("Selecione o tipo de problema do sistema:")
        for idx, problem in enumerate(SYSTEM_PROBLEM_TYPES, 1):
            print(f"{idx}. {problem}")
        problem_choice = int(input("Digite o número do tipo de problema: "))
        problem_type = SYSTEM_PROBLEM_TYPES[problem_choice - 1]

    else:
        print("Opção inválida. Por favor, tente novamente.")
        return

    # Comentário opcional
    if problem_choice != 4:
        comment = input("Escreva um comentário sobre o problema (opcional): ")
    # Comentário obrigatório(para "Outro" problema)
    else:
        comment = input("Escreva um comentário sobre o problema (obrigatório): ")

    # Cria um novo relatório de problema
    problem_report = ProblemReport(author_id=customer_id, machine_id=machine_id, problem_type=problem_type, comment=comment)
    
    # Salva o relatório de problema no banco de dados
    problem_report_dao = ProblemReportDAO(db_connection)
    problem_report_dao.insert_problem_report(problem_report)
    
    print("Problema reportado com sucesso!")
    time.sleep(2)

    
def create_customer_account(db_connection):
    """
    Create a new customer account.
    """
    clear_console()
    print("~"*10, "Criar Conta de Cliente:", "~"*10, "\n")

    name = input("Nome: ")
    email = input("Email: ")
    password = input("Senha: ")
    address = input("Endereço: ")
    anonymous_profile = input("Perfil anônimo (sim/não): ").strip().lower() == 'sim'
    
    # Cria um novo objeto Customer
    customer = UserFactory.create_user(user_type="Customer", name=name, email=email, password=password, address=address, anonymous_profile=anonymous_profile)
    
    # Insere o novo cliente no banco de dados
    customer_dao = CustomerDAO(db_connection)
    # Check if the 'customer' table exists and create it if necessary
    cursor = db_connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='customers';")
    table_exists = cursor.fetchone()

    if not table_exists:
        print("Creating the customer table as it does not exist.")
        customer_dao.create_table()
    
    customer_dao.insert_customer(customer)
    
    print("Conta de cliente criada com sucesso!")
    
    #para verificar se o cliente foi criado com sucesso e inserido na tabela customers
    """
    cursor.execute("SELECT * FROM customers")
    print(cursor.fetchall())
    """


def view_vending_machine_reviews(vending_machine_id, db_connection):
    """
        Display reviews for the selected vending machine.

    Parameters:
        vending_machine_id (str): The ID of the vending machine to retrieve reviews for.
        db_connection (sqlite3.Connection): The connection to the database.
    """
    clear_console()
    cursor = db_connection.cursor()

    # Verifique se a tabela de reviews existe
    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='reviews';
    """)
    table_exists = cursor.fetchone()

    if not table_exists:
        print("A tabela 'reviews' não existe. Nenhum comentário foi encontrado.")
        time.sleep(2)
        return

    # Buscar todos os comentários para a vending machine específica
    cursor.execute("""
        SELECT user_id, rating, comment, date FROM reviews WHERE machine_id = ?
    """, (vending_machine_id,))
    reviews = cursor.fetchall()

    if not reviews:
        print("\n>>> Nenhum comentário encontrado para esta vending machine. <<<")
        time.sleep(2)
        return

    # Organizar os dados dos reviews em um DataFrame para exibição
    reviews_data = {
        "Usuário": [],
        "Avaliação": [],
        "Comentário": [],
        "Data": []
    }

    for review in reviews:
        reviews_data["Usuário"].append(review[0])  # user_id
        reviews_data["Avaliação"].append(review[1])  # rating
        reviews_data["Comentário"].append(review[2])  # comment
        reviews_data["Data"].append(review[3])  # date

    df = pd.DataFrame(reviews_data)
    
    clear_console()
    print(f"\n~{'~'*10} Comentários da Máquina de Venda {'~'*10}\n")
    print(df.to_string(index=False))  # Exibe os comentários

    print("\nDigite 0 para voltar ao menu anterior.")
    input()  # Pausa para o usuário ler os comentários antes de voltar


def view_vending_machines_for_customer(db_connection):
    """
    Displays available vending machines, with name and location.

    Parameters:
        db_connection (sqlite3.Connection): The connection to the database.
    """

    vending_machine_dao = VendingMachineDAO(db_connection)

    # Check if the 'vending_machines' table exists and create it if necessary
    cursor = db_connection.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='vending_machines';
    """)
    table_exists = cursor.fetchone()

    if not table_exists:
        print("Creating the vending_machines table as it does not exist.")
        vending_machine_dao.create_table()

    # Buscar todas as vending machines
    vending_machines = vending_machine_dao.get_all_vending_machines()

    if not vending_machines:
        clear_console()
        print("~"*10, "Vending Machines Disponíveis", "~"*10)

        print("\n>>> Nenhuma vending machine disponível no momento. <<<")
        time.sleep(2)
        return

    # Organizar os dados em um DataFrame para exibição
    vending_machines_data = {
        "Index": [],
        "Nome": [],
        "Localização": []
    }
    
    for index, vm in enumerate(vending_machines, start=1):
        vending_machines_data["Index"].append(index)
        vending_machines_data["Nome"].append(vm.name)
        vending_machines_data["Localização"].append(vm.location)

    df = pd.DataFrame(vending_machines_data)
    
    while True:
        clear_console()
        print("~"*10, "Vending Machines Disponíveis", "~"*10)
        print(df.to_string(index=False))  # Exibir o DataFrame sem o índice automático do pandas
        
        selected_machine = input("\nDigite o número da máquina para ver os comentários ou 0 para voltar: ")

        try:
            selected_machine = int(selected_machine)

            if selected_machine == 0:
                return  # Volta ao menu anterior
            elif 1 <= selected_machine <= len(vending_machines):
                vending_machine_id = vending_machines[selected_machine - 1].id
                # Chama a função para visualizar os comentários (essa função será implementada separadamente)
                view_vending_machine_reviews(vending_machine_id, db_connection)
                break
            else:
                print("Número inválido. Escolha uma opção válida.")
                time.sleep(1)
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")
            time.sleep(1)


def create_review(customer_id, db_connection, review_dao, vending_machine_dao, product_dao):
    """
    Function to create a review for a product or vending machine.

    Parameters:
        customer_id (int): The ID of the customer making the review.
        db_connection (sqlite3.Connection): The connection to the database.
        review_dao (ReviewDAO): The data access object for interacting with the reviews table.
        vending_machine_dao (VendingMachineDAO): DAO for vending machines.
        product_dao (ProductDAO): DAO for products.
    """
    clear_console()
    print("\n", "~"*10, "Faça uma Avaliação", "~"*10, "\n")

    # Choose whether the review will be of a product or a vending machine
    review_type = input("Você gostaria de avaliar um produto (1) ou uma máquina de venda (2)? Digite o número correspondente: ")

    if review_type not in ["1", "2"]:
        print("Opção inválida. Retornando ao menu.")
        time.sleep(2)
        return

    # Get user rating
    try:
        rating = int(input("Dê uma nota de 0 a 5 para sua avaliação: "))
        if rating < 0 or rating > 5:
            raise ValueError("Nota deve estar entre 0 e 5.")
    except ValueError:
        print("Nota inválida. Deve ser um número entre 0 e 5.")
        time.sleep(2)
        return

    # Get comment (optional)
    comment = input("Deixe um comentário (opcional, pressione Enter para pular): ")
    if len(comment) > Review.MAX_COMMENT_LENGTH:
        print(f"Comentário muito longo. Deve ter no máximo {Review.MAX_COMMENT_LENGTH} caracteres.")
        return

    # Evaluating a product
    if review_type == "1":
        product_name = input("Digite o nome do produto que deseja avaliar: ")
        
        # Search for products with that name
        products = product_dao.get_products_by_name(product_name)

        if not products:
            print("Nenhum produto encontrado com esse nome.")
            time.sleep(2)
            return
        
        # Display the products found in a DataFrame
        product_data = {
            "Index": [],
            "Nome": [],
            "Descrição": [],
            "Preço": [],
            "Quantidade": []
        }

        for index, product in enumerate(products, start=1):
            product_data["Index"].append(index)
            product_data["Nome"].append(product.name)
            product_data["Descrição"].append(product.description)
            product_data["Preço"].append(product.price)
            product_data["Quantidade"].append(product.quantity)

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

        # Create product review
        review = Review(user_id=customer_id, rating=rating, comment=comment, product_id=selected_product_id)

    # Evaluating a Vending Machine
    elif review_type == "2":
        # Get Machine ID
        machine_name = input("Digite o nome da máquina de venda que deseja avaliar: ")

        # Search for machines with that name
        machines = vending_machine_dao.get_vending_machines_by_name(machine_name)

        if not machines:
            print("Nenhuma máquina encontrada com esse nome.")
            time.sleep(2)
            return
        
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
            print("Operação cancelada.")
            time.sleep(2)
            return

        # Get the selected machine and save the ID
        selected_machine_id = machines[selected_machine - 1].id

        # Create the machine review
        review = Review(user_id=customer_id, rating=rating, comment=comment, machine_id=selected_machine_id)

    #Insert the review into the database
    review_dao.insert_review(review)
    print("\n==> Sua avaliação foi registrada com sucesso!")
    time.sleep(2)


def customer_actions(customer_id, db_connection):    
    """
    Main function for the customer panel.
    """
    
    problem_report_dao = ProblemReportDAO(db_connection)
    review_dao = ReviewDAO(db_connection)
    product_dao = ProductDAO(db_connection)
    vending_machine_dao = VendingMachineDAO(db_connection)

    # Check if the 'problem_report' and 'reviews' tables exist and create them if necessary
    cursor = db_connection.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name IN ('problem_report', 'reviews', 'products', 'vending_machines');
    """)
    
    existing_tables = [table[0] for table in cursor.fetchall()]

    if 'problem_report' not in existing_tables:
        print("Creating the problem_report table as it does not exist.")
        problem_report_dao.create_table()
    
    if 'reviews' not in existing_tables:
        print("Creating the reviews table as it does not exist.")
        review_dao.create_table()

    if 'products' not in existing_tables:
        print("Creating the products table as it does not exist.")
        product_dao.create_table()
    
    if 'vending_machines' not in existing_tables:
        print("Creating the vending_machines table as it does not exist.")
        vending_machine_dao.create_table()
    
    while True:
        clear_console()
        print("~"*10, "Bem-vindo, Cliente!", "~"*10)

        print("1. Visualizar vending machines")
        print("2. Reportar problemas")
        print("3. Fazer uma avaliação (review)")
        print("0. Sair")
        escolha = input("Digite o número da ação: ")

        if escolha == "1":
            view_vending_machines_for_customer(db_connection)
        elif escolha == "2":
            create_problem_report(customer_id, db_connection)
        elif escolha == "3":
            create_review(customer_id, db_connection, review_dao, vending_machine_dao, product_dao)
        elif escolha == "0":
            print("\nSaindo do painel do usuário...")
            time.sleep(1)
            break
        else:
            print("\nOpção inválida. Tente novamente.")
            time.sleep(1)


