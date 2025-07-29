from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import func, insert, select, asc, desc
from sqlalchemy.orm import Session


class AbstractGetOneDAO(ABC):
    @abstractmethod
    def get_one(self, identifier_name: str, identifier_value: Any):
        raise NotImplementedError


class AbstractAddOneDAO(ABC):
    @abstractmethod
    def add_one(self, data: dict):
        raise NotImplementedError


class AbstractUpdateOneDAO(ABC):
    @abstractmethod
    def update_one(self, identifier: str, data: dict):
        raise NotImplementedError


class AbstractGetAllDAO(ABC):
    @abstractmethod
    def get_all(self):
        raise NotImplementedError


class AbstractDeleteOneDAO(ABC):
    @abstractmethod
    def delete_one(self):
        raise NotImplementedError


class AbstractGetPackDAO(ABC):
    @abstractmethod
    def get_pack(self, offset: int, limit: int):
        raise NotImplementedError


class ModelSession:
    model = None

    def __init__(self, session: Session):
        self.session = session


class AddOneItemDAO(ModelSession, AbstractAddOneDAO):
    def add_one(self, data: dict):
        query = insert(self.model).values(**data)
        self.session.execute(query)
        self.session.commit()


class GetOneItemDAO(ModelSession, AbstractGetOneDAO):
    def get_one(self, identifier_name: str, identifier_value: Any):
        query = select(self.model).where(getattr(self.model, identifier_name) == identifier_value)
        result = self.session.execute(query)
        return result.scalars().first()


class GetAllItemsDAO(ModelSession, AbstractGetAllDAO):
    def get_all(self):
        result = self.session.execute(select(self.model))
        return result.scalars().all()


class DeleteItemDAO(ModelSession, AbstractDeleteOneDAO):
    def delete_one(self, identifier_name: str, identifier_value: Any):
        item = self.get_one(identifier_name, identifier_value)
        if item:
            self.session.delete(item)
            self.session.commit()
        return item


class UpdateOneItemDAO(ModelSession, AbstractUpdateOneDAO):
    def update_one(self, identifier_name: str, identifier_value: Any, data: dict):
        updating_item = self.get_one(identifier_name, identifier_value)
        if updating_item:
            for key, value in data.items():
                setattr(updating_item, key, value)
            self.session.commit()
            return updating_item


class GetPackItemsDAO(ModelSession, AbstractGetPackDAO):
    def get_pack(self,
                 user_id: int,
                 page: int = 0,
                 limit: int = 14,
                 order_by: str = "date_time",
                 descending: bool = True,
                 ) -> list[dict[str, Any]]:
        offset = page * limit
        order_column = getattr(self.model, order_by)
        ordering = desc(order_column) if descending else asc(order_column)
        query = (select(self.model).
                 order_by(ordering).
                 limit(limit).
                 offset(offset)
                 )
        result = self.session.execute(query)
        return result.scalars().all()