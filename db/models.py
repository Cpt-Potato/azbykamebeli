from ormar import Integer, Model, String

from .base import database, metadata


class StraightSofas(Model):
    class Meta:
        tablename = "straight_sofas"
        database = database
        metadata = metadata

    id = Integer(primary_key=True)
    sku = String(max_length=50)
    item_id = Integer(index=True)
    title = String(max_length=255)
    full_price = Integer(nullable=True)
    sale_price = Integer()
    availability = String(max_length=50)
