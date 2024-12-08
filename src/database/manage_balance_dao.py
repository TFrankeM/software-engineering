import pandas as pd
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../classes")))
from money_deposit import MoneyDeposit

from customer_dao import CustomerDAO
from money_deposit_dao import MoneyDepositDAO

def clear_console():
    """
    Console clearing function, (just works in Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def manage_balance(customer_id, db_connection):
    """
    Manage the customer's balance: view or deposit money.

    Parameters:
        customer_id (int): The ID of the customer.
        db_connection (sqlite3.Connection): Database connection.
    """
    money_deposit_dao = MoneyDepositDAO(db_connection)

    while True:
        clear_console()
        print("~" * 10, "Saldo do Cliente", "~" * 10, "\n")

        print("1. Ver Saldo")
        print("2. Depositar Dinheiro")
        print("0. Voltar")
        escolha = input("\nDigite o número da ação: ")

        if escolha == "1":
            customer_dao = CustomerDAO(db_connection)
            total_balance = customer_dao.get_balance(customer_id)
            print(f"\nSeu saldo total é: R$ {total_balance:.2f}")
            input("\nPressione Enter para continuar...")

        elif escolha == "2":
            try:
                customer_dao = CustomerDAO(db_connection)
                amount = float(input("\nDigite o valor a ser depositado: R$ "))
                customer_dao.add_balance(customer_id, amount)
                print("\nDepósito realizado com sucesso!")
            except ValueError as e:
                print(f"\nErro: {str(e)}")
            input("\nPressione Enter para continuar...")

        elif escolha == "0":
            break
        else:
            print("\nOpção inválida. Tente novamente.")
            time.sleep(2)