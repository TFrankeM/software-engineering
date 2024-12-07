import pandas as pd
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../classes")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../database")))

from review_service import create_review 
from report_service import create_problem_report
from view_vending_machines import view_vending_machines_for_customer

from vending_machine_dao import VendingMachineDAO
from product_dao import ProductDAO
from problem_report_dao import ProblemReportDAO
from review_dao import ReviewDAO


def clear_console():
    """
    Console clearing function, (just works in Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')


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
        print("~"*10, "Bem-vindo, Cliente!", "~"*10, "\n")

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