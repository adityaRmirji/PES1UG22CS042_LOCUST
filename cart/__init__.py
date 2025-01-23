import json

import products
from cart import dao
from products import Product


class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data):
        return Cart(data['id'], data['username'], data['contents'], data['cost'])


def get_cart(username: str) -> list[Product]:
    # Retrieve cart details for the user
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    # Collect all product IDs from cart contents
    product_ids = []
    for cart_detail in cart_details:
        contents = cart_detail['contents']
        try:
            evaluated_contents = json.loads(contents)  # Replace eval with json.loads
        except json.JSONDecodeError:
            continue  # Skip invalid JSON entries
        product_ids.extend(evaluated_contents)

    # Fetch all products in a single batch call
    all_products = products.get_products_by_ids(product_ids)

    return all_products


def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    dao.delete_cart(username)

