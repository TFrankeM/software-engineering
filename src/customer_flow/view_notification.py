import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../classes")))
from notification import Notification

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../classes")))
from notification_dao import NotificationDAO

def clear_console():
    """
    Console clearing function, (Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def view_notification(customer_id, db_connection):
    """
    Function to view a customer's notifications.

    Parameters:
    customer_id (str): The ID of the customer whose notifications will be displayed.
    db_connection (sqlite3.Connection): Connection to the database.
    """
    notification_dao = NotificationDAO(db_connection)  # Instanciando a classe de persistência de notificações
    notifications_df = notification_dao.get_notifications_by_user(customer_id)

    clear_console()

    # Verifica se há notificações
    if notifications_df.empty:
        print("\n>>> Você não tem notificações.<<")
    else:
        # Exibe o título da seção
        print("~" * 10, " Suas Notificações ", "~" * 10, "\n")

        # Filtra e formata as colunas que queremos mostrar
        notifications_df = notifications_df[['notification_date', 'message']]  # Manter só a data e a mensagem
        notifications_df['notification_date'] = notifications_df['notification_date'].dt.strftime('%d/%m/%Y %H:%M:%S')  # Formatar a data

        # Exibe as notificações bonitinho
        for _, row in notifications_df.iterrows():
            print(f"\nData: {row['notification_date']}")
            print(f"Mensagem: {row['message']}")
            print("-" * 40)

    # Espera que o usuário pressione Enter para continuar
    input("\n==> Pressione Enter para voltar ao menu.")
