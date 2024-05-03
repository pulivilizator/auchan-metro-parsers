from .getter import json_getter


def get_products(store_id: int) -> list[tuple]:
    products_list = json_getter(store_id=store_id)
    products = [_get_parameters(product) for product in products_list]
    return products


def _get_parameters(product: dict) -> tuple:
    is_promo = product['stocks'][0]['prices_per_unit']['is_promo']
    return (
        product['id'],
        product['name'],
        'https://online.metro-cc.ru' + product['url'],
        product['stocks'][0]['prices_per_unit']['price'],
        product['stocks'][0]['prices_per_unit'][
            'old_price'] if is_promo else '-',
        product['manufacturer']['name']
    )
