import threading
import asyncio

from parser import CSVWriter, get_products
from metro_parser.settings import MOSCOW_SHOP_IDS, SAINT_PETERSBURG_SHOP_IDS


def main(shop_ids: list[int],
         csv_path: str = 'data.csv'):
    products = asyncio.run(get_products(shop_ids))
    writer = CSVWriter(products=products,
                       path=csv_path,
                       mode='w')
    writer.writerows()


if __name__ == '__main__':
    moscow_thread = threading.Thread(target=main,
                                     args=(MOSCOW_SHOP_IDS,
                                           'moscow.csv'))

    saint_petersburg_thread = threading.Thread(target=main,
                                               args=(SAINT_PETERSBURG_SHOP_IDS,
                                                     'saint_petersburg.csv'))

    moscow_thread.start()
    saint_petersburg_thread.start()

    moscow_thread.join()
    saint_petersburg_thread.join()
