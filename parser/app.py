import asyncio
from time import sleep

import requests
from bs4 import BeautifulSoup

from db.base import database
from db.models import StraightSofas
from parser.base import get_availability, get_item_id, get_prices, get_sku, get_title

base_url = "https://azbykamebeli.ru"
url = "https://azbykamebeli.ru/catalog/0000057/"


async def parse_and_save_data(session) -> None:
    for page_number in range(1, 26):
        parsed_page_data = []
        print(f"Page {page_number}/25")
        page_url = f"https://azbykamebeli.ru/catalog/0000057/?page={page_number}"
        response = session.get(page_url)
        soup = BeautifulSoup(response.text, "lxml")
        items = soup.select("div.items-list > div > div > div")
        sleep(2)

        for item in items:
            sku = get_sku(item)
            item_id = get_item_id(item)
            title = get_title(item)
            full_price, sale_price = get_prices(item)
            availability = get_availability(item)
            parsed_item_data = StraightSofas(
                sku=sku,
                item_id=item_id,
                title=title,
                full_price=full_price,
                sale_price=sale_price,
                availability=availability,
            )
            parsed_page_data.append(parsed_item_data)
        await write_to_db(parsed_page_data)


async def write_to_db(data) -> None:
    await StraightSofas.objects.bulk_create(data)


async def main() -> None:
    session = requests.Session()
    async with database:
        await parse_and_save_data(session)


if __name__ == "__main__":
    asyncio.run(main())
