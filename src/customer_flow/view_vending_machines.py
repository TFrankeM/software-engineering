import pandas as pd
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../database")))

from vending_machine_dao import VendingMachineDAO


def clear_console():
    """
    Console clearing function, (just works in Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')

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
