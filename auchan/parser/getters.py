import bs4
from aiohttp import ClientSession

from .utils import get_html_page
from auchan.settings import MAIN_URL


async def get_urls(session: ClientSession, region_id: int, qrator_key: str) -> \
        list[str]:
    html_page = await get_html_page(session=session,
                                    region_id=region_id,
                                    qrator_key=qrator_key)
    soup = bs4.BeautifulSoup(html_page, 'html.parser')
    pages = soup.find(class_='css-gmuwbf').find_all('li')
    max_page = max([int(page.text) for page in pages if page.text.isdigit()])
    return [f'{MAIN_URL}?page={page}' for page in range(1, max_page + 1)]
