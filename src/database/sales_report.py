import sqlite3
import os
from transaction_dao import TransactionDAO
from item_transaction_dao import ItemTransactionDAO
import csv

def clear_console():
    """
    Console clearing function, (Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_report(query, file_name, connection):
    """
    Executa uma consulta SQL, exibe os resultados no terminal e pergunta se deseja salvar em um arquivo CSV.

    Parameters:
        query (str): Consulta SQL para gerar o relatório.
        file_name (str): Nome do arquivo para salvar o relatório.
        connection (sqlite3.Connection): Conexão com o banco de dados.
    """
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            print("\nNenhum dado encontrado para os filtros aplicados.")
            return

        # Obter os títulos das colunas
        column_names = [description[0] for description in cursor.description]

        # Exibindo os resultados no terminal
        clear_console()
        print("\n=== Resultados do Relatório ===")
        print("\t".join(column_names))
        for row in results:
            print("\t".join(map(str, row)))

        # Pergunta ao usuário se deseja salvar
        save_option = input("\nDeseja salvar o relatório em um arquivo CSV? (s/n): ").lower()
        if save_option == 's':
            with open(file_name, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(column_names)  # Escrever os títulos das colunas
                writer.writerows(results)  # Escrever os dados
            print(f"Relatório salvo como: {file_name}")
        else:
            print("Relatório não foi salvo.")

    except sqlite3.Error as e:
        print(f"Erro ao gerar o relatório: {e}")


def report_transactions_with_filters(connection):
    """
    Gera um relatório de transações com filtros personalizados.
    """
    clear_console()
    print("\n=== Relatório de Transações com Filtros ===")
    filters = []

    # Filtros dinâmicos
    if input("Filtrar por data? (s/n): ").lower() == 's':
        start_date = input("Data inicial (AAAA-MM-DD): ")
        end_date = input("Data final (AAAA-MM-DD): ")
        filters.append(f"transaction_date BETWEEN '{start_date}' AND '{end_date}'")

    if input("Filtrar por comprador? (s/n): ").lower() == 's':
        user_id = input("ID do comprador: ")
        filters.append(f"user_id = '{user_id}'")

    if input("Filtrar por vendedor? (s/n): ").lower() == 's':
        seller_id = input("ID do vendedor: ")
        filters.append(f"seller_id = '{seller_id}'")

    if input("Filtrar por máquina de venda? (s/n): ").lower() == 's':
        machine_id = input("ID da máquina: ")
        filters.append(f"vending_machine_id = '{machine_id}'")

    # Construção da cláusula WHERE
    where_clause = " AND ".join(filters) if filters else "1=1"

    # Escolha do foco do relatório
    focus = input("\nO que você deseja analisar? (vendedor/comprador/máquina/geral): ").strip().lower()

    if focus == "vendedor":
        query = f"""
        SELECT sellers.name AS Vendedor, COUNT(t.id) AS Total_Vendas, SUM(t.total_amount) AS Total_Receita
        FROM transactions t
        JOIN sellers ON t.seller_id = sellers.id
        WHERE {where_clause}
        GROUP BY sellers.name
        ORDER BY Total_Receita DESC;
        """
    elif focus == "comprador":
        query = f"""
        SELECT customers.name AS Comprador, COUNT(t.id) AS Total_Compras, SUM(t.total_amount) AS Total_Gasto
        FROM transactions t
        JOIN customers ON t.user_id = customers.id
        WHERE {where_clause}
        GROUP BY customers.name
        ORDER BY Total_Gasto DESC;
        """
    elif focus == "máquina":
        query = f"""
        SELECT machines.name AS Maquina, COUNT(t.id) AS Total_Vendas, SUM(t.total_amount) AS Total_Receita
        FROM transactions t
        JOIN vending_machines machines ON t.vending_machine_id = machines.id
        WHERE {where_clause}
        GROUP BY machines.name
        ORDER BY Total_Receita DESC;
        """
    elif focus == "geral":
        query = f"""
        SELECT t.transaction_date AS Data, customers.name AS Comprador, sellers.name AS Vendedor, machines.name AS Maquina, t.total_amount AS Total
        FROM transactions t
        JOIN customers ON t.user_id = customers.id
        JOIN sellers ON t.seller_id = sellers.id
        JOIN vending_machines machines ON t.vending_machine_id = machines.id
        WHERE {where_clause}
        ORDER BY t.transaction_date ASC;
        """
    else:
        print("Opção inválida! Retornando ao menu principal.")
        return

    file_name = f"relatorio_{focus}.csv"
    generate_report(query, file_name, connection)


def main_menu(db_connection):
    """
    Menu principal para o sistema de relatórios.
    """
    while True:
        clear_console()
        print("\n=== Menu de Relatórios ===")
        print("1. Relatório de transações")
        print("2. Sair")

        choice = input("Escolha uma opção: ")

        if choice == '1':
            report_transactions_with_filters(db_connection)
        elif choice == '2':
            print("Saindo...")
            break
        else:
            print("Opção inválida! Tente novamente.")