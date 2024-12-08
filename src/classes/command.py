from item_transaction import ItemTransaction
from transaction import Transaction

class Command:
    def execute(self):
        pass


class AddToCartCommand(Command):
    def __init__(self, shopping_cart, product_id, quantity, products):
        """
        Initialize the calss.

        Parameters:
            shopping_cart (dict): The shopping cart dictionary.
            product_id (int): The ID of the product being added.
            quantity (int): The quantity of the product being added.
            products (list): The list of products available.

        """
        self.shopping_cart = shopping_cart
        self.product_id = product_id
        self.quantity = quantity
        self.products = products


    def execute(self):
        """
        Execute the AddToCartCommand.

        If the product is already in the shopping cart, increment the quantity.
        Otherwise, add the product to the cart.

        """
        if self.product_id in self.shopping_cart:
            self.shopping_cart[self.product_id] += self.quantity
        else:
            self.shopping_cart[self.product_id] = self.quantity
        print(f"Produto {self.products[self.product_id - 1].name} adicionado ao carrinho, quantidade: {self.quantity}")


class RemoveFromCartCommand(Command):
    def __init__(self, shopping_cart, product_id):
        """
        Initialize the  class.

        Parameters:
            shopping_cart (dict): The shopping cart dictionary.
            product_id (str): The ID of the product to be removed from the cart.
        """
        self.shopping_cart = shopping_cart
        self.product_id = product_id

    def execute(self):
        """
        Execute the remove from cart command.

        If the product ID is found in the shopping cart dictionary, it will be removed.
        Otherwise, a message will be printed indicating that the product was not found in the cart.
        """
        if self.product_id in self.shopping_cart:
            del self.shopping_cart[self.product_id]
            print(f"Produto removido do carrinho.") 
        else: 
            print(f"Produto não encontrado no carrinho.")


class CheckoutCommand(Command):
    def __init__(self, shopping_cart, customer_id, products, vending_machine_owner_id, vending_machine_id, vending_machine_name, 
                 customer_dao, seller_dao, transaction_dao, item_transaction_dao, favorite_product_dao, product_dao):
        """
        Initializes a new instance of the CheckoutCommand class.

        Args:
            shopping_cart (dict): A dictionary representing the shopping cart with product IDs as keys and quantities as values.
            customer_id (int): The ID of the customer making the purchase.
            products (list): A list of Product objects.
            vending_machine_owner_id (str): The owner's id of the vending machine.
            vending_machine_id(str): The id of the vending machine.
            vending_machine_name (str): The name of the vending machine.
            customer_dao (CustomerDAO): An instance of the CustomerDAO class.
            seller_dao (SellerDAO): An instance of the SellerDAO class.
            transaction_dao (TransactionDAO): An instance of the TransactionDAO class.
            item_transaction_dao (ItemTransactionDAO): An instance of the ItemTransactionDAO class.
            favorite_product_dao (FavoriteProductDAO): An instance of the FavoriteProductDAO class.
            product_dao (ProductDAO): An instance of the ProductDAO class.
        """
        self.shopping_cart = shopping_cart
        self.customer_id = customer_id
        self.products = products
        self.vending_machine_owner_id = vending_machine_owner_id
        self.vending_machine_id = vending_machine_id
        self.vending_machine_name = vending_machine_name
        self.customer_dao = customer_dao
        self.seller_dao = seller_dao
        self.transaction_dao = transaction_dao
        self.item_transaction_dao = item_transaction_dao
        self.favorite_product_dao = favorite_product_dao
        self.product_dao = product_dao


    def execute(self):
        """
        Executes the checkout command.

        This method calculates the total value of the purchase, checks if the customer has enough coins to complete the purchase,
        deducts the coins from the customer, transfers the purchase value to the seller, updates the stock, notifies observers
        if a product is out of stock, creates and saves the transaction, and prints a success message with the total amount paid.
        """
        print("\nFinalizando a compra...")

        total_value = sum(self.products[product_id - 1].price * quantity for product_id, quantity in self.shopping_cart.items())

        customer_coins = self.customer_dao.get_balance(self.customer_id)

        if customer_coins < total_value:
            print("\nVocê não tem crétidos suficientes para finalizar a compra.")
            return
 
        self.customer_dao.add_balance(self.customer_id, -(total_value))
        print("Cliente cobrado!")

        seller = self.seller_dao.get_seller_by_id(self.vending_machine_owner_id)

        self.seller_dao.add_balance(self.vending_machine_owner_id, total_value)
        print("Vendedor pago!")

        for product_id, quantity in self.shopping_cart.items():
            product = self.products[product_id - 1]
            new_quantity = product.quantity - quantity
            self.product_dao.update_product_quantity(product.id, new_quantity)

            if new_quantity == 0:
                self.favorite_product_dao.notify_observers(product.id, f"O produto '{product.name}' da loja '{self.vending_machine_name}' ficou sem estoque!")

        transaction = Transaction(user_id=self.customer_id,
                                  seller_id=self.vending_machine_owner_id,
                                  vending_machine_id = self.vending_machine_id,
                                  total_amount=total_value)
        transaction_id = self.transaction_dao.insert_transaction(transaction)

        for product_id, quantity in self.shopping_cart.items():
            product = self.products[product_id - 1]
            item_transaction = ItemTransaction(transaction_id=transaction_id,
                                               product_id=product.id,
                                               quantity=quantity,
                                               price=product.price)
            self.item_transaction_dao.insert_item_transaction(item_transaction)

        print(f"Compra finalizada com sucesso! Total pago: R$ {total_value:.2f}")


class ShoppingCartInvoker:
    def __init__(self):
        self.commands = []

    def set_command(self, command: Command):
        """
        Sets the command to be executed in the shopping cart invoker.

        Args:
            command (Command): The command to be executed.
        """
        self.commands.append(command)


    def execute_commands(self):
        """
        Executes all the commands in the shopping cart invoker.
        """
        for command in self.commands:
            command.execute()


    def execute_last_command(self):
        """
        Execute only the last command in the list.
        """
        if self.commands:
            self.commands[-1].execute()


    def __str__(self):
        return "ShoppingCartInvoker"