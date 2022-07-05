from pydantic import BaseModel


class InfoModelBase(BaseModel):
    sku: str
    item_id: int
    title: str
    full_price: int | None
    sale_price: int
    availability: str


class InfoModelOut(InfoModelBase):
    id: int


class UpdateInfoModel(InfoModelBase):
    sku: str | None
    item_id: int | None
    title: str | None
    full_price: int | None
    sale_price: int | None
    availability: str | None
