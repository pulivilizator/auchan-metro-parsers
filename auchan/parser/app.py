from aiohttp import ClientSession

from .handlers.products_handlers import products_process
from .handlers.id_handlers import products_id_process
from .writer import CSVWriter


async def app(qrator_key: str, csv_path: str, region_id: int):
    async with ClientSession() as session:
        products_id = await products_id_process(session=session,
                                                qrator_key=qrator_key,
                                                region_id=region_id)
        products = await products_process(session=session,
                                          products_id=products_id)
    writer = CSVWriter(products=products,
                       path=csv_path,
                       mode='w')
    writer.writerows()
