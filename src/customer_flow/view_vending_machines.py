import pandas as pd
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../database")))

from vending_machine_dao import VendingMachineDAO
from review_dao import ReviewDAO
from product_dao import ProductDAO
from customer_dao import CustomerDAO

def clear_console():
    """
    Console clearing function, (just works in Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def view_vending_machine_products(customer_id, vending_machine, db_connection):
    """
    Displays the available products in a vending machine and allows the user to add items to the cart.
    
    Parameters:
        customer_id (str): The ID of the customer whose notifications will be displayed.
        vending_machine (class): id, name, location, owner_id (seller).
        db_connection (sqlite3.Connection): The connection to the database.
    """
    clear_console()

    # Create DAO instances
    product_dao = ProductDAO(db_connection)
    
    # Get products for the vending machine
    products = product_dao.get_products_by_vending_machine_id(vending_machine.id)
    
    if not products:
        print(f"\n>>> Nenhum produto encontrado para '{vending_machine.name}' <<<")
        
        input("\n==> Pressione Enter para voltar ao menu.")
        return
    
    # Organize the product data into a DataFrame for display
    products_data = {
        "Index": [],
        "Nome": [],
        "Preço": [],
        "Quantidade": [],
        "Descrição": []
    }
    
    for index, product in enumerate(products, start=1):
        products_data["Index"].append(index)
        products_data["Nome"].append(product.name)
        products_data["Preço"].append(f"R$ {product.price:.2f}")
        products_data["Quantidade"].append(product.quantity)
        products_data["Descrição"].append(product.description)
    
    # Display the products as a DataFrame
    products_df = pd.DataFrame(products_data)
    
     # Carrinho de compras (armazenando produtos e quantidades)
    shopping_cart = {}  # {product_id: quantity}

    while True:
        clear_console()
        title = "~" * 10 + f" Produtos de '{vending_machine.name}' " + "~" * 10 + "\n"

        print(title)
        print(products_df.to_string(index=False))  # Display the products without index

        # Exibir o valor total da compra
        total_value = sum(products[product_id - 1].price * quantity for product_id, quantity in shopping_cart.items())
        print("~"*len(title))
        print(f"\nValor total da compra: R$ {total_value:.2f}")
        
        # Exibir o carrinho
        if shopping_cart:
            print("\nCarrinho de Compras:")
            for product_id, quantity in shopping_cart.items():
                product = products[product_id - 1]
                print(f"{product.name} - Quantidade: {quantity} - Preço unitário: R$ {product.price:.2f}")
        
        # Ask the user for input
        print("~"*len(title))
        print("\nDigite o número do produto seguido pela quantidade desejada: '<opção>x<quantidade>' para adicionar ao carrinho")
        print("Por exemplo, para escolher duas unidades da opção 3, seria: '3x2'\n")
        print("Digite '1000' para finalizar a compra e seguir para pagamento")
        print("\nDigite 0 para cancelar e voltar ao menu anterior.")
        print("~"*len(title))
        
        choice = input("\nO que você deseja fazer? ")

        if choice == "0":
            return

        elif choice == "1000":
            # Aqui você chamaria a função de transação (ex: transaction_service)
            print("\nFinalizando a compra...")
            return

        try:
            # Parse input to get product index and quantity
            product_index, quantity = choice.split('x')
            product_index = int(product_index.strip())
            quantity = int(quantity.strip())
            
            if 1 <= product_index <= len(products) and quantity > 0:
                product = products[product_index - 1]  # Get the product by index
                if quantity > product.quantity:
                    print("\nQuantidade solicitada maior do que a disponível. Tente novamente.")
                else:
                    # Adiciona o produto ao carrinho
                    if product_index in shopping_cart:
                        shopping_cart[product_index] += quantity  # Incrementa a quantidade no carrinho
                    else:
                        shopping_cart[product_index] = quantity  # Adiciona o produto ao carrinho

                    # Add the product to the cart (you would implement the cart handling here)
                    print(f"\nProduto {product.name} adicionado ao carrinho, quantidade: {quantity}")
                    # Atualize o carrinho aqui (adicionar produto com a quantidade desejada)
                    input("\n==> Pressione Enter para escolher novamente.")

            else:
                print("\nÍndice ou quantidade inválida. Tente novamente.")
                time.sleep(1)
        except ValueError:
            print("\nEntrada inválida. Tente novamente.")
            time.sleep(1)

    
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
        clear_console()
        print("~"*10, "Detalhes da Vending Machines", "~"*10)


        print(f"\nNome: {vending_machine.name}")
        print(f"Localição: {vending_machine.location}\n")
        
        #print(f"1. {} máquina da lista de favoritos")
        print("2. Ver produtos disponíveis")
        print("3. Ver Histórico de Avaliações")
        print("0. Voltar")

        escolha = input("\nDigite o número correspondente: ")
        
        if escolha == "1":
            pass
            # Adicionar a lista de favoritos
        elif escolha == "2":
            view_vending_machine_products(customer_id, vending_machine, db_connection)
        elif escolha == "3":
            # Chama a função para visualizar os comentários (essa função será implementada separadamente)
            view_vending_machine_reviews(vending_machine, db_connection)
            
        elif escolha == "0":
            return
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
