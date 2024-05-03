import asyncio
from aiohttp import ClientSession

from itertools import chain

from .getter import json_getter


async def get_products(shop_ids: list[int]) -> set:
    async with ClientSession() as session:
        raw_products = await asyncio.gather(
            *[
                asyncio.create_task(_get_products_for_shop(store_id, session))
                for store_id in shop_ids
            ]
        )
        products = chain.from_iterable(raw_products)
        return set(products)


async def _get_products_for_shop(store_id: int, session: ClientSession) -> list[tuple]:
    products_list = await json_getter(store_id=store_id, session=session)
    products = [_get_parameters(product) for product in products_list]
    return products


def _get_parameters(product: dict) -> tuple:
    is_promo = product['stocks'][0]['prices_per_unit']['is_promo']
    return (
        product['id'],
        product['name'],
        'https://online.metro-cc.ru' + product['url'],
        product['stocks'][0]['prices_per_unit']['price'],
        product['stocks'][0]['prices_per_unit']['old_price'] if is_promo else '-',
        product['manufacturer']['name']
    )
