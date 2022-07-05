import requests
from bs4 import BeautifulSoup
from time import sleep

base_url = "https://azbykamebeli.ru"
url = "https://azbykamebeli.ru/catalog/0000057/"
session = requests.Session()


def get_number_of_pages(session) -> int:
    response = session.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    number_of_pages = int(
        soup.select_one("ul.pagination li.page-item:nth-child(7) a.page-link")
        .get_text()
    )
    return number_of_pages


def parse_data(session) -> None:
    for page_number in range(1, 26):
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
            SKU = soup.select_one("div.info-container div.align-self-start span:nth-child(1)").get_text().split(": ")[1]
            ID = soup.select_one("div.info-container div.align-self-start span:nth-child(2)").get_text().split(": ")[1]
            price = int(soup.select_one("div.row div.col-12.col-md-8.d-flex.justify-content-between a.store-price.fake-link").get_text()[:-2].replace(" ", ""))
            price_discount = int(soup.select_one("div.row div.online-price").get_text()[:-2].replace(" ", ""))
            availability = soup.select_one("div.pt-1.mt-1.pb-1 div.col-sm-8.m-auto div.btn:nth-child(1)").get_text().strip()
            return
