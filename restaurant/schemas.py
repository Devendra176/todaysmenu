from pydantic import BaseModel
from typing import List, Optional, Union


# Restaurant Schemas
from restaurant.menu.schemas import Menu


class RestaurantBase(BaseModel):
    name: str
    description: Optional[str] = None
    phone: Union[str, None]


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantCreateResponse(RestaurantCreate):
    id: int


class AddressBase(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str
    latitude: float
    longitude: float


class AddressDetails(AddressBase):
    id: int

    class Config:
        from_attributes = True


class AddressCreate(AddressBase):
    pass


class OwnerBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: Union[str, None]

    class Config:
        from_attributes = True


class OwnerDetail(OwnerBase):
    id: int


class RestaurantDetail(RestaurantBase):
    id: int
    menus: List[Menu] = []
    owner: OwnerDetail
    addresses: Optional[List[AddressDetails]] = None

    class Config:
        from_attributes = True


class Owner(OwnerBase):
    id: int
    restaurants: List[RestaurantDetail] = []

    class Config:
        from_attributes = True


class RestaurantList(RestaurantDetail):
    pass