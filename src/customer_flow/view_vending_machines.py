import pandas as pd
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../classes")))
from favorite_machine import FavoriteMachine

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../database")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../classes")))

from transaction import Transaction
from item_transaction import ItemTransaction
from transaction_service import view_and_buy_vending_machine_products

from favorite_product_machine_dao import FavoriteMachineDAO
from vending_machine_dao import VendingMachineDAO
from review_dao import ReviewDAO
from product_dao import ProductDAO
from customer_dao import CustomerDAO
from seller_dao import SellerDAO
from transaction_dao import TransactionDAO
from item_transaction_dao import ItemTransactionDAO

def clear_console():
    """
    Console clearing function, (just works in Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')

    
def view_vending_machine_reviews(vending_machine, db_connection):
    """
        Display reviews for the selected vending machine.

    Parameters:
        vending_machine (class): id, name, location, owner_id (seller).
        db_connection (sqlite3.Connection): The connection to the database.
    """
    clear_console()

    review_dao = ReviewDAO(db_connection)
    customer_dao = CustomerDAO(db_connection)

    # Get the reviews for the vending machine using the method get_reviews_for_machine
    reviews = review_dao.get_reviews_for_machine(vending_machine.id)

    if not reviews:
        print(f"\n>>> Nenhum comentário encontrado para '{vending_machine.name}' <<<")
        
        input("\n==> Pressione Enter para voltar ao menu.")
        return

    # Organizar os dados dos reviews em um DataFrame para exibição
    reviews_data = {
        "Usuário": [],
        "Avaliação": [],
        "Comentário": [],
        "Data": []
    }

    for review in reviews:
        # Retrieve customer details to get the name
        customer = customer_dao.get_customer_by_id(review.user_id)
        
        if customer:
             # If the customer's profile is private, display "Anônimo"
            user_name = customer.name if not customer.anonymous_profile else "Anônimo"
        else:
            user_name = "Anônimo"  # If no customer found, consider as anonymous

        reviews_data["Usuário"].append(user_name)
        reviews_data["Avaliação"].append(review.rating)
        reviews_data["Comentário"].append(review.comment)
        reviews_data["Data"].append(review.date)

    df = pd.DataFrame(reviews_data)
    
    clear_console()
    print(f"\n~{'~'*10} Comentários da Máquina de Venda {'~'*10}\n")
    print(df.to_string(index=False))  # Exibe os comentários

    input("\n==> Pressione Enter para voltar ao menu.")
    

def vending_machine_details(customer_id, vending_machine, db_connection):
    """
    Display details of a vending machine and provide options to perform actions.
    
    Parameters:
        customer_id (str): The ID of the customer whose notifications will be displayed.
        vending_machine: an object representing a vending machine
        db_connection: a database connection object
    
    Returns:
    None
    """
    
    while True:
        # Instanciando o DAO para verificar favoritos
        favorite_machine_dao = FavoriteMachineDAO(db_connection)
        
        # Verificando se a máquina está nos favoritos
        favorite = favorite_machine_dao.is_favorite_machine(customer_id, vending_machine.id)
        
        clear_console()
        print("~"*10, "Detalhes da Vending Machines", "~"*10)

        print(f"\nNome: {vending_machine.name}")
        print(f"Localização: {vending_machine.location}\n")
        
        # Se a máquina estiver nos favoritos, mostrar a opção para removê-la, caso contrário, mostrar para adicionar
        if favorite:
            print(f"1. Remover máquina da lista de favoritos")
        else:
            print(f"1. Adicionar máquina na lista de favoritos")
        
        print("2. Ver produtos disponíveis")
        print("3. Ver Histórico de Avaliações")
        print("0. Voltar")

        escolha = input("\nDigite o número correspondente: ")

        if escolha == "1":
            clear_console()
            if favorite:
                # Se a máquina está nos favoritos, removemos
                favorite_machine_dao.detach(customer_id, vending_machine.id)
                print("\nMáquina removida da lista de favoritos.")
            else:
                # Se a máquina não está nos favoritos, adicionamos
                # O método attach exige um objeto FavoriteMachine
                favorite_machine_dao.attach(FavoriteMachine(customer_id, vending_machine.id))  
                print("\nMáquina adicionada à lista de favoritos.")
            input("\n==> Pressione Enter para escolher novamente.")

        elif escolha == "2":
            view_and_buy_vending_machine_products(customer_id, vending_machine, db_connection)
        elif escolha == "3":
            # Visualizar Histórico de Avaliações
            view_vending_machine_reviews(vending_machine, db_connection)
            
        elif escolha == "0":
            return  # Voltar ao menu anterior
        else:
            print("\rOpção inválida. Tente novamente.", flush=True)
            time.sleep(2)


def view_vending_machines_for_customer(customer_id, db_connection):
    """
    Displays available vending machines, with name and location.

    Parameters:
        customer_id (str): The ID of the customer whose notifications will be displayed.
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
        
        input("\n==> Pressione Enter para voltar ao menu.")

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
        
        selected_machine = input("\nDigite o número da máquina para ver mais opções ou 0 para voltar: ")

        try:
            selected_machine = int(selected_machine)

            if selected_machine == 0:
                return  # Volta ao menu anterior
            elif 1 <= selected_machine <= len(vending_machines):
                vending_machine_details(customer_id, vending_machines[selected_machine - 1], db_connection)
            else:
                print("Número inválido. Escolha uma opção válida.")
                time.sleep(1.5)
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")
            time.sleep(1.5)
