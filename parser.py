import requests
from bs4 import BeautifulSoup
from time import sleep

base_url = "https://azbykamebeli.ru"
url = "https://azbykamebeli.ru/catalog/0000057/"


# Not used, but maybe helpful if there will be more or less than 25 pages
def get_number_of_pages(session) -> int:
    response = session.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    number_of_pages = int(
        soup.select_one(
            "ul.pagination li.page-item:nth-child(7) a.page-link"
        ).get_text()
    )
    return number_of_pages


def write_to_db(data) -> None:
    pass


def parse_data(session) -> None:
    for page_number in range(1, 26):
        parsed_page_data = []
        page_url = f"https://azbykamebeli.ru/catalog/0000057/?page={page_number}"
        response = session.get(page_url)
        soup = BeautifulSoup(response.text, "lxml")
        all_item_links = soup.select("div.items-list div.row div.item__title.h4 a")
        sleep(2)

        for item in all_item_links:
            item_link = base_url + item["href"]
            response = session.get(item_link)
            soup = BeautifulSoup(response.text, "lxml")

            title = soup.select_one("div.container.type-page h1").get_text()
            sku = (
                soup.select_one(
                    "div.info-container div.align-self-start span:nth-child(1)"
                )
                .get_text()
                .split(": ")[1]
            )
            id_ = (
                soup.select_one(
                    "div.info-container div.align-self-start span:nth-child(2)"
                )
                .get_text()
                .split(": ")[1]
            )
            full_price = int(
                soup.select_one(
                    "div.row div.col-12.col-md-8.d-flex.justify-content-between a.store-price.fake-link"
                )
                .get_text()[:-2]
                .replace(" ", "")
            )
            sale_price = int(
                soup.select_one("div.row div.online-price")
                .get_text()[:-2]
                .replace(" ", "")
            )
            availability = (
                soup.select_one(
                    "div.pt-1.mt-1.pb-1 div.col-sm-8.m-auto div.btn:nth-child(1)"
                )
                .get_text()
                .strip()
            )
            if availability == "Купить":
                availability = "Доступно"
            else:
                availability = "Под заказ"

            # parsed_page_data.update({
            #     "title": title,
            #     "SKU": sku,
            #     "ID": id_,
            #     "full_price": full_price,
            #     "sale_price": sale_price,
            #     "availability": availability
            # })
            # write_to_db(parsed_page_data)
            parsed_page_data.append(
                [title, sku, id_, full_price, sale_price, availability]
            )
            return
        write_to_db(parsed_page_data)


if __name__ == "__main__":
    session = requests.Session()
    parse_data(session)
