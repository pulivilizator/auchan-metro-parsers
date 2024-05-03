import time
from aiohttp import ClientSession
from fake_useragent import UserAgent
from playwright.sync_api import sync_playwright

from auchan.settings import MAIN_URL
from .exceptions import QratorIdFailedToRetrieve


async def get_html_page(session: ClientSession,
                        qrator_key: str,
                        region_id: int,
                        url=None) -> str:
    if url is None:
        url = MAIN_URL
    ua = UserAgent()
    cookies = {
        'region_id': str(region_id),
        'qrator_jsid': qrator_key,
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'User-Agent': ua.random,
    }
    async with session.get(url,
                           cookies=cookies,
                           headers=headers) as response:
        html_page = await response.text(encoding='utf-8-sig')
    return html_page


def get_qrator_jsid_cookie() -> str:
    with sync_playwright() as p:
        browser = p.firefox.launch()
        page = browser.new_page()
        qrator_key = check_cookies(page)
        browser.close()
        return qrator_key


def check_cookies(page):
    count = 0
    while True:
        page.goto(MAIN_URL)
        time.sleep(3)
        cookies = page.context.cookies()
        for cookie in cookies:
            if cookie['name'] == 'qrator_jsid':
                return cookie['value']
        count += 1
        if count == 10:
            raise QratorIdFailedToRetrieve
