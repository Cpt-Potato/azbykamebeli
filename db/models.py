from sqlalchemy import Table, Column, Integer, String

from .base import metadata

straight_sofas = Table(
    "straight_sofas",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(length=50)),
    Column("item_id", Integer),
    Column("title", String(length=255)),
    Column("full_price", Integer),
    Column("sale_price", Integer),
    Column("availability", String(length=50)),
)
