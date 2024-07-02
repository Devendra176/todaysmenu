from abc import ABC
from typing import List, Dict

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session


class BaseManager(ABC):
    model = None
    read_only_fields = ['id']

    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return list(self.db.query(self.model).all())

    def get_by_id(self, _id: int):
        return self.db.query(self.model).get(_id)

    def update_by_id(self, _id: int, data: Dict):
        self.db.query(self.model).filter(self.model.id == _id).update(data)
        self.db.commit()

    def save_all(self, data: List[Dict]):
        self.db.add_all([self.model(**item) for item in data])
        self.db.commit()

    def save_all_with_skip_duplicate(self, data: List[Dict]):
        self.db.execute(insert(self.model).values(data).on_conflict_do_nothing())
        self.db.commit()
