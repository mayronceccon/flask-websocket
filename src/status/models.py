from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.db.engine import Engine
from src.db.base import Base
from src.db.session import Session

BaseInstance = Base.get_instance()


class Status(BaseInstance):
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(50))
    description = Column(String(50))

    @classmethod
    def find_all(cls, page=1):
        offset = 0

        if (page > 1):
            offset = page * 10

        return Session.get_instance() \
            .query(cls) \
            .limit(10) \
            .offset(offset) \
            .all() \

    @property
    def serialize(self):
        return {
            'id': self.id,
            'slug': self.slug,
            'description': self.description,
        }

    def __repre__(self):
        return self.description
