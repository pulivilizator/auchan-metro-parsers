import enum
from typing import NamedTuple

MAIN_URL = 'https://www.auchan.ru/catalog/konditerskie-izdeliya/konfety-karamel/shokoladnye/'
API_URL = 'https://api.retailrocket.ru/api/1.0/partner/5ecce55697a525075c900196/items/'


class CityId(enum.Enum):
    moscow = 1
    saint_petersburg = 2


class Price(NamedTuple):
    regular_price: float
    promo_price: float | str
