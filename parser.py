import asyncio
import requests
from bs4 import BeautifulSoup
from time import sleep

from db.base import database
from db.models import straight_sofas

base_url = "https://azbykamebeli.ru"
url = "https://azbykamebeli.ru/catalog/0000057/"


async def write_to_db(data) -> None:
    query = straight_sofas.insert()
    await database.execute_many(query=query, values=data)


def get_sku(item):
    return item.select_one("div.item__description > div.d-flex.justify-content-between > small.text-muted.f-XS").get_text().split(": ")[1]


async def parse_data(session) -> None:
    for page_number in range(2, 3):
        print(f"Page {page_number}/25")
        parsed_page_data = []
        page_url = f"https://azbykamebeli.ru/catalog/0000057/?page={page_number}"
        # response = session.get(page_url)
        # soup = BeautifulSoup(response.text, "lxml")
        with open("page.html", encoding="utf-8") as f:
            response = f.read()
        soup = BeautifulSoup(response, "lxml")
        sleep(2)
        items = soup.select("div.items-list > div > div > div")
        for item in items:
            sku = (
                item.select_one(
                    "div.item__description > div.d-flex.justify-content-between > small.text-muted.f-XS"
                )
                .get_text()
                .split(": ")[1]
            )
            item_id = int(
                item.select_one(
                    "div.items-list > div > div > div > div.item__description > div.item__title.h4 > a"
                )["href"]
                .split("/")[-1]
                .split("=")[-1]
            )
            title_base = item.select_one(
                "div.items-list > div > div > div > div.item__description > div.item__title.h4 > a > span"
            ).get_text()
            title_additional = item.select_one(
                "div.items-list > div > div > div > div.item__description > p:last-child"
            ).get_text()
            if not title_additional:
                title_additional = item.select_one(
                    "div.items-list > div > div > div > div.item__description > p:nth-last-child(-n+2)"
                ).get_text()
            try:
                full_price = int(
                    item.select_one(
                        "div.items-list > div > div > div > div.item__footer.mt-auto > div > div > div.price > a.store-price.fake-link"
                    )
                    .get_text()[:-2]
                    .replace(" ", "")
                )
            except AttributeError:
                full_price = None
            sale_price = int(
                item.select_one(
                    "div.items-list > div > div > div > div.item__footer.mt-auto > div > div > div.price > div.online-price"
                )
                .get_text()[:-2]
                .replace(" ", "")
            )
            availability = (
                item.select_one(
                    "div.items-list > div > div > div > div.item__description > div.d-flex.justify-content-between > small.f-XS.d-inline-block.badge.badge-pill"
                )
                .get_text()
                .capitalize()
            )
            parsed_item_data = {
                "sku": sku,
                "item_id": item_id,
                "title": f"{title_base} {title_additional}",
                "full_price": full_price,
                "sale_price": sale_price,
                "availability": availability,
            }
            parsed_page_data.append(parsed_item_data)
        await write_to_db(parsed_page_data)


async def main() -> None:
    session = requests.Session()
    async with database:
        await parse_data(session)


if __name__ == "__main__":
    asyncio.run(main())
