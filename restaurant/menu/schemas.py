from typing import List, Optional

from fastapi import UploadFile
from pydantic import BaseModel


# Restaurant Menu's Schema's
class MenuBase(BaseModel):
    name: str
    description: str
    todaysmenu: bool = False


class MenuItemImageBase(BaseModel):
    url: str


class MenuItemImageCreate(BaseModel):
    pass


class MenuItemImageCreateUpload(UploadFile):
    url: str


class MenuItemImageCreateUploadRes(BaseModel):
    menu_item_id: int
    urls: List[str]
    success: bool = False


class MenuItemImage(MenuItemImageBase):
    id: int

    class Config:
        from_attributes = True


class MenuItemBase(BaseModel):
    name: str
    description: str
    price: int


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemCreateResponse(MenuItemBase):
    id: int


class MenuItem(MenuItemBase):
    id: int
    images: List[MenuItemImage] = []

    class Config:
        from_attributes = True


class MenuCreate(MenuBase):
    pass


class MenuCreateResponse(MenuBase):
    id: int


class Menu(MenuBase):
    id: int
    items: List[MenuItem] = []

    class Config:
        from_attributes = True
