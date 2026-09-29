from enum import Enum

from sqlmodel import Field, SQLModel


class StatusEnum(str, Enum):
    LOST = "Lost"
    FOUND = "Found"
    RETURNED = "Returned"


class ItemBase(SQLModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=5)
    category: str = Field(min_length=1)
    location: str = Field(min_length=1)
    reported_by: str = Field(min_length=1)
    status: StatusEnum


class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass