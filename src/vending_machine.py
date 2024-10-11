class Vending_Machine:
    """
        first version of the product class
    """
    def __init__(self, name, id, location):
        self.name = name
        self.id = id
        self.location = location
        self.products = {}

    def add_product(self, product, quantity):
        if product.id in self.products:
            self.products[product.id].update_quantity(quantity)
        else:
            product.update_quantity(quantity)
            self.products[product.id] = product
        
    def list_products(self):
        return [str(product.name) for product in self.products.values()]
    
    def check_stock(self, product_id):
        if product_id in self.products:
            return self.products[product_id].quantity
        return 0
    