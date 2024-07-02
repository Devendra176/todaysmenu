import os
from typing import List
from uuid import uuid4

from fastapi import UploadFile

from core.exceptions import ExceptionHandling
from core.managers import BaseManager
from core.settings import api_settings
from restaurant.models import Restaurant, Menu, MenuItemImage, MenuItem, Address


class BaseRestaurantOperationManager(BaseManager):
    def create(self, obj: dict):
        ob = None
        try:
            ob = self.model(**obj)
            self.db.add(ob)
            self.db.commit()
        except Exception as e:
            print(e)
        return ob

    def get_by_name(self, name: str):
        pass


class RestaurantManager(BaseRestaurantOperationManager):
    model = Restaurant


class AddressManager(BaseRestaurantOperationManager):
    model = Address


class MenuManager(BaseRestaurantOperationManager):
    model = Menu


class MenuItemManager(BaseRestaurantOperationManager):
    model = MenuItem


class MenuItemImageManager(BaseRestaurantOperationManager):
    model = MenuItemImage

    def save(self, files, menu_item):
        obj = []
        res = {
            'menu_item_id': menu_item.id,
            'urls': [],
            'success': False
        }
        try:
            for file in files:
                fb = self.model(
                        url=file,
                        menu_item_id=menu_item.id,
                        menu_item=menu_item,
                    )
                obj.append(fb)
                res['urls'].append(file)
            self.db.bulk_save_objects(obj)
            self.db.commit()
            res['success'] = True
            return res
        except Exception as e:
            self.db.rollback()
            raise ExceptionHandling(detail=str(e))
