import asyncio
import threading

from parser.app import app
from parser.utils import get_qrator_jsid_cookie
from settings import CityId


def main(region_id: int, csv_path: str):
    qrator_key = get_qrator_jsid_cookie()
    asyncio.run(app(qrator_key=qrator_key,
                    csv_path=csv_path,
                    region_id=region_id))


if __name__ == '__main__':
    moscow_thread = threading.Thread(target=main,
                                     args=(CityId.moscow.value,
                                           f'{CityId.moscow.name}.csv'))

    saint_petersburg_thread = threading.Thread(target=main,
                                               args=(
                                                   CityId.saint_petersburg.value,
                                                   f'{CityId.saint_petersburg.name}.csv'))

    moscow_thread.start()
    saint_petersburg_thread.start()

    moscow_thread.join()
    saint_petersburg_thread.join()
