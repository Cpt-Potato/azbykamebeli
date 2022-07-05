from sqlalchemy import Table, Column, Integer, String

from .base import metadata

straight_sofas = Table(
    "straight_sofas",
    metadata,
    Column("sku", Integer, primary_key=True, index=True, unique=True),
    Column("id", Integer),
    Column("title", String(length=100)),
    Column("full_price", Integer),
    Column("sale_price", Integer),
    Column("availability", String(length=50)),
)
