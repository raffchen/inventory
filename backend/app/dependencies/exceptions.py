class ProductsNotFound(Exception):
    def __init__(self):
        super().__init__("No products found")


class ProductNotFound(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id
        super().__init__(f"Product with ID {product_id} not found")


class ProductAlreadyExists(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id
        super().__init__(f"Product with ID {product_id} already exists")
