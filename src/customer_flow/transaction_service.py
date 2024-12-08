import pandas as pd
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../database")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../classes")))

from transaction import Transaction
from item_transaction import ItemTransaction
from favorite_product import FavoriteProduct
from command import ShoppingCartInvoker, CheckoutCommand, AddToCartCommand

from vending_machine_dao import VendingMachineDAO
from review_dao import ReviewDAO
from product_dao import ProductDAO
from customer_dao import CustomerDAO
from seller_dao import SellerDAO
from transaction_dao import TransactionDAO
from item_transaction_dao import ItemTransactionDAO
from favorite_product_machine_dao import FavoriteProductDAO

def clear_console():
    """
    Console clearing function, (just works in Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def view_and_buy_vending_machine_products(customer_id, vending_machine, db_connection):
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
    customer_dao = CustomerDAO(db_connection)
    seller_dao = SellerDAO(db_connection)                       # Accessing the Seller table
    transaction_dao = TransactionDAO(db_connection)
    item_transaction_dao = ItemTransactionDAO(db_connection)
    favorite_product_dao = FavoriteProductDAO(db_connection)    # Instance for managing favorite products

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
        "Avaliação Média": [],
        "Descrição": [],
        "Favorito": []
    }
    
    for index, product in enumerate(products, start=1):
        # Check if the product is a favorite for the customer
        is_favorite = favorite_product_dao.is_favorite_product(customer_id, product.id)
        
        products_data["Index"].append(index)
        products_data["Nome"].append(product.name)
        products_data["Preço"].append(f"R$ {product.price:.2f}")
        products_data["Quantidade"].append(product.quantity)
        products_data["Avaliação Média"].append(product.average_rating)
        products_data["Descrição"].append(product.description)
        products_data["Favorito"].append("Sim" if is_favorite else "Não")  #Sim se é favorito, Não cc
    

    # Display the products as a DataFrame
    products_df = pd.DataFrame(products_data)
    
    # Carrinho de compras (armazenando produtos e quantidades)
    shopping_cart = {}  # {product_id: quantity}

    invoker = ShoppingCartInvoker()

    while True:
        clear_console()
        title = "~" * 10 + f" Produtos de '{vending_machine.name}' " + "~" * 10 + "\n"

        print(title)
        print(products_df.to_string(index=False))  # Display the products without index

        # Exibir o valor total da compra
        total_value = sum(products[product_id - 1].price * quantity for product_id, quantity in shopping_cart.items())
        print("~"*len(title)*2)
        print(f"\nValor total da compra: R$ {total_value:.2f}")
        
        # Exibir o carrinho
        if shopping_cart:
            print("\nCarrinho de Compras:")
            for product_id, quantity in shopping_cart.items():
                product = products[product_id - 1]
                print(f"{product.name} - Quantidade: {quantity} - Preço unitário: R$ {product.price:.2f}")
        
        # Ask the user for input
        print("~"*len(title)*2)
        print(">>>> Opções <<<<")
        print("\n- Digite o número do produto seguido pela quantidade desejada: '<opção>x<quantidade>' para adicionar ao carrinho")
        print("Por exemplo, para escolher duas unidades da opção 3, seria: '3x2'\n")
        print("- Digite '1000' para finalizar a compra e seguir para pagamento")
        print("- Digite o índice do produto para adicioná-lo ou removê-lo da lista de favoritos")
        print("\n- Digite 0 para cancelar e voltar ao menu anterior.")
        print("~"*len(title)*2)
        
        choice = input("\nO que você deseja fazer? ")

        #### SAIR
        if choice == "0":
            return

        #### PAGAR
        elif choice == "1000":
            # Finalizar a compra
            checkout_command = CheckoutCommand(
                shopping_cart,
                customer_id,
                products,
                vending_machine.owner_id,
                vending_machine.id,
                vending_machine.name,
                customer_dao,
                seller_dao,
                transaction_dao,
                item_transaction_dao,
                favorite_product_dao,
                product_dao
            )
            
            checkout_command.execute()

            input("\n==> Pressione Enter para voltar ao menu.")
            return

        try:
        # ADCIONAR NOVO PRODUTO AO CARRINHO
            if "x" in choice:
                # Parse input to get product index and quantity
                product_index, quantity = choice.split('x')
                product_index = int(product_index.strip())
                quantity = int(quantity.strip())
                
                if 1 <= product_index <= len(products) and quantity > 0:
                    product = products[product_index - 1]  # Get the product by index

                    # Verificar a quantidade total no carrinho
                    current_quantity_in_cart = shopping_cart.get(product_index, 0)  # Se não tiver no carrinho, será 0

                    if current_quantity_in_cart + quantity > product.quantity:
                        print("\nQuantidade solicitada maior do que a disponível. Tente novamente.")
                    else:
                        add_command = AddToCartCommand(shopping_cart, product_index, quantity, products)
                        invoker.set_command(add_command)
                        invoker.execute_last_command()

                    input("\n==> Pressione Enter para continuar.")
                else: 
                    input("\n==> Ìndice inválido. Pressione Enter para escolher novamente")

        #### ADICIONAR/REMOVER DOS FAVORITOS 
            # Verificar se o número escolhido está dentro do intervalo válido de produtos
            elif int(choice) > 0 and int(choice) <= len(products_df):
                product = products[int(choice) - 1]  # Obter o produto correspondente
                is_favorite = favorite_product_dao.is_favorite_product(customer_id, product.id)  # Verificar se é favorito
                
                if is_favorite:
                    # Remover do favorito
                    favorite_product_dao.detach(customer_id, product.id)
                    products_df.loc[int(choice) - 1, "Favorito"] = "Não"
                    print(f"\n{product.name} removido dos favoritos.")
                else:
                    # Adicionar aos favoritos
                    favorite_product_dao.attach(FavoriteProduct(customer_id, product.id))
                    products_df.loc[int(choice) - 1, "Favorito"] = "Sim"
                    print(f"\n{product.name} adicionado aos favoritos.")

                input("\n==> Pressione Enter para continuar.")
        

            else:
                print("\nÍndice ou quantidade inválida. Tente novamente.")
                time.sleep(1)
        except ValueError:
            print("\nEntrada inválida. Tente novamente.")
            time.sleep(1)