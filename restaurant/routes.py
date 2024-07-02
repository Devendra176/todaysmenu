from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.exceptions import RestaurantNotFoundError
from core.utils import get_db
from restaurant.managers import RestaurantManager, AddressManager
from restaurant.schemas import RestaurantCreate, AddressCreate, RestaurantDetail, AddressBase, \
    RestaurantList, RestaurantCreateResponse, AddressDetails
from user.dependencies import get_current_restaurant_owner
from user.models import User

router = APIRouter()


# Restaurant Routes
@router.get("/list")
def list_resturants(db: Session = Depends(get_db)) -> List[RestaurantList]:
    restaurants = RestaurantManager(db).get_all()
    return [RestaurantList.from_orm(i) for i in restaurants]


@router.post("/register")
def register(current_user: Annotated[User, Depends(get_current_restaurant_owner)],
             restaurant_data: RestaurantCreate, db: Session = Depends(get_db)) \
        -> RestaurantCreateResponse:
    restaurant = restaurant_data.dict()
    restaurant.update({'owner_id': current_user.id})
    restaurant = RestaurantManager(db).create(restaurant)
    return RestaurantCreateResponse(**restaurant.as_dict())


@router.get("/{restaurant_id}")
def get_restaurant(restaurant_id: int,
                   # current_user: Annotated[User, Depends(get_current_restaurant_owner)],
                   db: Session = Depends(get_db)) -> RestaurantDetail:
    restaurant = RestaurantManager(db).get_by_id(restaurant_id)
    if not restaurant:
        raise RestaurantNotFoundError
    return RestaurantDetail.from_orm(restaurant)


@router.post("/{restaurant_id}/address")
def add_address(restaurant_id: int,
                # current_user: Annotated[User, Depends(get_current_restaurant_owner)],
                address_data: AddressCreate,
                db: Session = Depends(get_db)) -> AddressDetails:
    restaurant = RestaurantManager(db).get_by_id(restaurant_id)
    if not restaurant:
        raise RestaurantNotFoundError
    address = address_data.dict()
    address.update({'restaurant_id': restaurant_id})
    address = AddressManager(db).create(address)
    return AddressDetails(**address.as_dict())


@router.put("/{restaurant_id}/")
def update_restaurant(restaurant_id: int,
                      # current_user: Annotated[User, Depends(get_current_restaurant_owner)],
                      restaurant_data: RestaurantCreate, db: Session = Depends(get_db)) \
        -> RestaurantCreateResponse:
    restaurant_manager = RestaurantManager(db)
    restaurant = restaurant_manager.get_by_id(restaurant_id)
    if not restaurant:
        raise RestaurantNotFoundError
    restaurant_manager.update_by_id(restaurant_id, restaurant_data.dict())
    return RestaurantCreateResponse(**restaurant.as_dict())


@router.put("/{address_id}/address")
def update_address(address_id: int,
                   # current_user: Annotated[User, Depends(get_current_restaurant_owner)],
                   address_data: AddressBase, db: Session = Depends(get_db)) -> AddressDetails:
    address_manager = AddressManager(db)
    address = address_manager.get_by_id(address_id)
    if not address:
        raise RestaurantNotFoundError
    address_manager.update_by_id(address_id, address_data.dict())
    return AddressDetails(**address.as_dict())
