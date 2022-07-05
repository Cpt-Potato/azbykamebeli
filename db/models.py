from sqlalchemy import Table, Column, Integer, String

from .setup import metadata

straight_sofas = Table(
    "straight_sofas",
    metadata,
    Column("title", String(length=100)),
    Column("sku", Integer, primary_key=True, index=True),
    Column("id", Integer),
    Column("full_price", Integer),
    Column("sale_price", Integer),
    Column("availability"),
)
