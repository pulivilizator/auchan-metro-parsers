import asyncio
import random
from itertools import chain

from aiohttp import ClientSession
from fake_useragent import UserAgent

from auchan.settings import API_URL, Price


async def products_process(products_id: list[int], session: ClientSession) -> set[tuple]:
    raw_products = await asyncio.gather(
        *[
            asyncio.create_task(current_product_process(product_id=product_id,
                                                        session=session))
            for product_id in products_id
        ]
    )
    return set(i for i in raw_products if i)


async def current_product_process(product_id: int,
                                  session: ClientSession) -> tuple | bool:
    await asyncio.sleep(random.uniform(.5, 5))
    ua = UserAgent()
    headers = {
        'user-agent': ua.random
    }

    params = {
        'itemsIds': str(product_id),
        'stock': '1',
    }
    async with session.get(API_URL, params=params,
                           headers=headers) as response:
        product = await response.json()
    if not product or not product[0]['IsAvailable']:
        return False
    price = price_process(product)
    return (
        product[0]['ItemId'],
        product[0]['Name'],
        product[0]['Url'],
        price.regular_price,
        price.promo_price,
        brand_process(product),
    )


def price_process(product: list[dict]) -> Price:
    regular_price = product[0]['OldPrice']
    promo_price = product[0]['Price']

    if not regular_price:
        regular_price = promo_price
        promo_price = '-'
        return Price(regular_price=round(regular_price, 2),
                     promo_price=promo_price)
    return Price(regular_price=round(regular_price, 2),
                 promo_price=round(promo_price, 2))


def brand_process(product: list[dict]):
    brand = product[0]['Vendor']
    if brand:
        return brand
    name = product[0]['Name']
    return name.split('«')[1].split('»')[0] if '«' in name and '»' in name else '-'