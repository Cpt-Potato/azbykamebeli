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
