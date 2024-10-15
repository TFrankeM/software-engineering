
class Product:
    """
        first version of the product class
    """
    def __init__(self, name, id, price, quantity):
        self.name = name
        self.id = id
        self.price = price
        self.quantity = quantity


    def update_quantity(self, new_quantity):
        self.quantity = new_quantity
    