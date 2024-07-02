from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from core.exceptions import RestaurantNotFoundError, MenuNotFoundError, MenuItemNotFoundError
from core.utils import get_db
from restaurant.dependencies import RestaurantContentTypeChecker
from restaurant.managers import RestaurantManager, MenuManager, MenuItemManager, \
    MenuItemImageManager
from restaurant.menu.schemas import MenuCreate, MenuItemCreate, \
    MenuCreateResponse, MenuItemCreateResponse, MenuItemImageCreateUpload, MenuItemImage, \
    MenuItemImageCreateUploadRes

router = APIRouter()
restaurant_content_type_checker = RestaurantContentTypeChecker()


@router.post("/{restaurant_id}/menu")
def add_menu(restaurant_id: int,
             # current_user: Annotated[User, Depends(get_current_restaurant_owner)],
             menu_data: MenuCreate, db: Session = Depends(get_db)) -> MenuCreateResponse:
    restaurant_manager = RestaurantManager(db)
    restaurant = restaurant_manager.get_by_id(restaurant_id)
    if not restaurant:
        raise RestaurantNotFoundError
    menu = menu_data.dict()
    menu.update({'restaurant_id': restaurant_id})
    obj = MenuManager(db).create(menu)
    return MenuCreateResponse(**obj.as_dict())


@router.get("/{menu_id}")
def get_menu(menu_id: int,
             # current_user: Annotated[User, Depends(get_current_restaurant_owner)],
             menu_data: MenuCreate, db: Session = Depends(get_db)):
    pass


@router.get("/{menu_item_id}")
def get_item(menu_item_id: int,
             # current_user: Annotated[User, Depends(get_current_restaurant_owner)],
             item_data: MenuItemCreate, db: Session = Depends(get_db)):
    pass


@router.post("/{menu_id}/menu/item")
def add_item(menu_id: int,
             # current_user: Annotated[User, Depends(get_current_restaurant_owner)],
             item_data: MenuItemCreate, db: Session = Depends(get_db)) -> MenuItemCreateResponse:
    menu = MenuManager(db).get_by_id(menu_id)
    if not menu:
        raise MenuNotFoundError

    menu_item = item_data.dict()
    menu_item.update({'menu_id': menu_id})
    menu_item = MenuItemManager(db).create(menu_item)
    return MenuItemCreateResponse(**menu_item.as_dict())


@router.post("/{menu_item_id}/images")
async def add_item_image(menu_item_id: int,
                         # current_user: Annotated[User, Depends(get_current_restaurant_owner)],
                         images: list[MenuItemImageCreateUpload] =
                         Depends(restaurant_content_type_checker),
                         db: Session = Depends(get_db)) -> MenuItemImageCreateUploadRes:
    menu_item = MenuItemManager(db).get_by_id(menu_item_id)
    if not menu_item:
        raise MenuItemNotFoundError
    files = await restaurant_content_type_checker.save_files(images)
    menu_item_images = MenuItemImageManager(db).save(files, menu_item)
    return MenuItemImageCreateUploadRes(**menu_item_images)

