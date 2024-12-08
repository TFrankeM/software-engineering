import sqlite3
import os
from transaction_dao import TransactionDAO
from item_transaction_dao import ItemTransactionDAO

def generate_report(query, file_name, db_connection):
    """
    SQL query, that show the results on terminal and asks if you want to save it in a txt flie.

    Parameters:
        query (str): SQL query.
        file_name (str): File name.
        connection (sqlite3.Connection): Database conection.
    """
    try:
        cursor = db_connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            print("\nNenhum dado encontrado para os filtros aplicados.")
            return

        # Exibindo os resultados no terminal
        print("\n=== Resultados do Relatório ===")
        for row in results:
            print("\t".join(map(str, row)))

        # Pergunta ao usuário se deseja salvar
        save_option = input("\nDeseja salvar o relatório em um arquivo? (s/n): ").lower()
        if save_option == 's':
            with open(file_name, "w") as file:
                for row in results:
                    file.write("\t".join(map(str, row)) + "\n")
            print(f"Relatório salvo como: {file_name}")
        else:
            print("Relatório não foi salvo.")

    except sqlite3.Error as e:
        print(f"Erro ao gerar o relatório: {e}")
        
    