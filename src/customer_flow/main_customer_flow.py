import pandas as pd
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../classes")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../database")))

from review_service import create_review 
from report_service import create_problem_report
from view_vending_machines import view_vending_machines_for_customer
from view_notification import view_notification

from vending_machine_dao import VendingMachineDAO
from product_dao import ProductDAO
from problem_report_dao import ProblemReportDAO
from review_dao import ReviewDAO
from notification_dao import NotificationDAO
from favorite_product_machine_dao import FavoriteMachineDAO, FavoriteProductDAO
from transaction_dao import TransactionDAO
from item_transaction_dao import ItemTransactionDAO
from manage_balance_dao import manage_balance

def clear_console():
    """
    Console clearing function, (just works in Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def customer_actions(customer_id, db_pool):    
    """
    Main function for the customer panel.
    """
    
    db_connection = db_pool.get_connection()         # Pega uma conexão do pool

    problem_report_dao = ProblemReportDAO(db_connection)
    review_dao = ReviewDAO(db_connection)
    product_dao = ProductDAO(db_connection)
    vending_machine_dao = VendingMachineDAO(db_connection)
    notification_dao = NotificationDAO(db_connection)
    favorite_machines_dao = FavoriteMachineDAO(db_connection)
    favorite_products_dao = FavoriteProductDAO(db_connection)
    transactions_dao = TransactionDAO(db_connection)
    item_transactions_dao = ItemTransactionDAO(db_connection)

    # Check if the 'problem_report' and 'reviews' tables exist and create them if necessary
    cursor = db_connection.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name IN ('problem_report', 'reviews', 'products', 'vending_machines', 
                   'notification', 'favorite_machines', 'favorite_products', 'transactions', 'item_transactions');
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

    if 'notification' not in existing_tables:
        print("Creating the notification table as it does not exist.")
        notification_dao.create_table()
    
    if 'favorite_machines' not in existing_tables:
        print("Creating the favorite_machines table as it does not exist.")
        favorite_machines_dao.create_table()

    if 'favorite_products' not in existing_tables:
        print("Creating the favorite_products table as it does not exist.")
        favorite_products_dao.create_table()

    if 'transactions' not in existing_tables:
        print("Creating the transactions table as it does not exist.")
        transactions_dao.create_table()
    
    if 'item_transactions' not in existing_tables:
        print("Creating the item_transactions table as it does not exist.")
        item_transactions_dao.create_table()

    while True:
        clear_console()
        print("~"*10, "Bem-vindo, Cliente!", "~"*10, "\n")

        print("1. Visualizar vending machines")
        print("2. Notificações")
        print("3. Reportar problemas")
        print("4. Fazer uma avaliação (review)")
        print("5. Gerenciar saldo")
        print("0. Sair")
        escolha = input("\nDigite o número da ação: ")

        if escolha == "1":
            view_vending_machines_for_customer(customer_id, db_connection)
        elif escolha == "2":
            view_notification(customer_id, db_connection)
        elif escolha == "3":
            create_problem_report(customer_id, db_connection)
        elif escolha == "4":
            create_review(customer_id, db_connection, review_dao, vending_machine_dao, product_dao)
        elif escolha == "5":
            manage_balance(customer_id, db_connection)
        elif escolha == "0":
            break
        else:
            print("\nOpção inválida. Tente novamente.")
            time.sleep(1)
    
    db_pool.release_connection(db_connection)        # Devolve a conexão ao pool
