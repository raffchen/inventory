class ProductsNotFound(Exception):
    def __init__(self):
        super().__init__("No products found")


class ProductNotFound(Exception):
    def __init__(self, product_id: int):
        super().__init__(f"Product with ID {product_id} not found")


class ProductAlreadyExists(Exception):
    def __init__(self, product_id: int):
        super().__init__(f"Product with ID {product_id} already exists")


class MalformedInput(Exception):
    def __init__(self, message: str):
        super().__init__(message)
