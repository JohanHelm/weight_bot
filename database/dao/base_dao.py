from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import and_, asc, desc, func, insert, select
from sqlalchemy.orm import Session


class AbstractGetOneDAO(ABC):
    @abstractmethod
    def get_one(self, identifiers: dict[str, Any]):
        raise NotImplementedError


class AbstractAddOneDAO(ABC):
    @abstractmethod
    def add_one(self, data: dict):
        raise NotImplementedError


class AbstractUpdateOneDAO(ABC):
    @abstractmethod
    def update_one(self, identifier: str, data: dict):
        raise NotImplementedError


class AbstractDeleteOneDAO(ABC):
    @abstractmethod
    def delete_one(self):
        raise NotImplementedError


class AbstractGetPackDAO(ABC):
    @abstractmethod
    def get_pack(self, user_id: int, page: int, limit: int):
        raise NotImplementedError


class AbstractGetAwgDAO(ABC):
    @abstractmethod
    def get_awg_data(self,
                     user_id: int,
                     page: int,
                     limit: int,
                     identifier_name: str,
                     ):
        raise NotImplementedError


class AbstractGetCountDAO(ABC):
    @abstractmethod
    def get_count(self, user_id: int,):
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
    def get_one(self, identifiers: dict[str, Any]):
        conditions = [getattr(self.model, key) == value for key, value in identifiers.items()]
        query = select(self.model).where(and_(*conditions))
        result = self.session.execute(query)
        return result.scalars().first()


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
                 page: int,
                 limit: int,
                 order_by: str = "date",
                 descending: bool = True,
                 ) -> list[dict[str, Any]]:

        offset = page * limit
        order_column = getattr(self.model, order_by)
        ordering = desc(order_column) if descending else asc(order_column)

        query = (select(self.model).
                 where(self.model.user_id == user_id).
                 order_by(ordering).
                 limit(limit * 2).
                 offset(offset)
                 )

        result = self.session.execute(query)
        return result.scalars().all()


class GetAwgDataDAO(ModelSession, AbstractGetAwgDAO):
    def get_awg_data(self,
                     user_id: int,
                     page: int,
                     limit: int,
                     identifier_name: str,
                     order_by: str = "date",
                     descending: bool = True,
                     ) -> float | None:

        offset = page * limit
        order_column = getattr(self.model, order_by)
        ordering = desc(order_column) if descending else asc(order_column)

        subqu = (
            select(getattr(self.model, identifier_name))
            .where(self.model.user_id == user_id)
            .order_by(ordering)
            .limit(limit)
            .offset(offset)
            .subquery()
        )

        query = select(func.avg(subqu.c[identifier_name]))
        result = self.session.execute(query)
        return result.scalar()


class GetCountItemsDAO(ModelSession, AbstractGetCountDAO):
    def get_count(self, user_id: int,):
        query = (
            select(func.count())
            .select_from(self.model)
            .where(self.model.user_id == user_id)
        )
        result = self.session.execute(query)
        return result.scalar()
