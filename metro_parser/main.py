import threading

from parser import CSVWriter, get_products


def main(store_id: int = 308,
         csv_path: str = 'data.csv'):
    products = get_products(store_id)
    writer = CSVWriter(products=products,
                       path=csv_path,
                       mode='w')
    writer.writerows()


if __name__ == '__main__':
    moscow_thread = threading.Thread(target=main,
                                     args=(308, 'moscow.csv'))

    saint_petersburg_thread = threading.Thread(target=main,
                                               args=(16, 'saint_petersburg.csv'))

    moscow_thread.start()
    saint_petersburg_thread.start()

    moscow_thread.join()
    saint_petersburg_thread.join()