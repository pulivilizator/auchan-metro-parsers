import asyncio
from itertools import chain

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from ..getters import get_urls
from ..utils import get_html_page


async def products_id_process(session: ClientSession,
                              qrator_key: str,
                              region_id: int):
    urls = await get_urls(session=session,
                          region_id=region_id,
                          qrator_key=qrator_key)
    products_id = await asyncio.gather(
        *[
            asyncio.create_task(_current_page_ids_process(session, qrator_key, url, region_id))
            for url in urls
        ]
    )
    return chain.from_iterable(products_id)


async def _current_page_ids_process(session: ClientSession,
                                    qrator_key: str,
                                    url: str,
                                    region_id: int) -> list[int]:

    html_page = await get_html_page(session=session,
                                    qrator_key=qrator_key,
                                    url=url,
                                    region_id=region_id)
    soup = BeautifulSoup(html_page, 'html.parser')
    products = soup.find_all('div', class_='css-n9ebcy-Item')
    return [product.get('data-offer-id') for product in products]
