import asyncio
import requests
from bs4 import BeautifulSoup
from time import sleep

from db.base import database
from db.models import straight_sofas

base_url = "https://azbykamebeli.ru"
url = "https://azbykamebeli.ru/catalog/0000057/"


async def parse_and_save_data(session) -> None:
    for page_number in range(17, 26):
        print(f"Page {page_number}/25")
        parsed_page_data = []
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
            parsed_item_data = {
                "sku": sku,
                "item_id": item_id,
                "title": title,
                "full_price": full_price,
                "sale_price": sale_price,
                "availability": availability,
            }
            parsed_page_data.append(parsed_item_data)
        await write_to_db(parsed_page_data)


def get_sku(item) -> str:
    return (
        item.select_one(
            "div.item__description > div.d-flex.justify-content-between > small.text-muted.f-XS"
        )
        .get_text()
        .split(": ")[1]
    )


def get_item_id(item) -> int:
    return int(
        item.select_one(
            "div.items-list > div > div > div > div.item__description > div.item__title.h4 > a"
        )["href"]
        .split("/")[-1]
        .split("=")[-1]
    )


def get_title(item) -> str:
    title_base = item.select_one(
        "div.items-list > div > div > div > div.item__description > div.item__title.h4 > a > span"
    ).get_text()
    title_additional = item.select_one(
        "div.items-list > div > div > div > div.item__description > p:last-child"
    ).get_text()
    if not title_additional:
        title_additional = item.select_one(
            "div.items-list > div > div > div > div.item__description > p:nth-child(4)"
        ).get_text()
    return f"{title_base} {title_additional}"


def get_prices(item) -> tuple[int | None, int]:
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
    return full_price, sale_price


def get_availability(item):
    return (
        item.select_one(
            "div.items-list > div > div > div > div.item__description > div.d-flex.justify-content-between > small.f-XS.d-inline-block.badge.badge-pill"
        )
        .get_text()
        .capitalize()
    )


async def write_to_db(data) -> None:
    query = straight_sofas.insert()
    await database.execute_many(query=query, values=data)


async def main() -> None:
    session = requests.Session()
    async with database:
        await parse_and_save_data(session)


if __name__ == "__main__":
    asyncio.run(main())
