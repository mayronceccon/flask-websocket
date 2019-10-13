from sqlalchemy import Column, ForeignKey, Integer, String, Text, \
    DateTime
from sqlalchemy.orm import relationship
from src.db.engine import Engine
from src.db.base import Base
from src.db.session import Session
from src.status.models import Status

BaseInstance = Base.get_instance()


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return value.strftime("%Y-%m-%d %H:%M:%S")


class Task(BaseInstance):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(100))
    description = Column(Text)
    expected_date = Column(DateTime)
    status_id = Column(Integer, ForeignKey('status.id'))
    status = relationship(Status)

    @classmethod
    def get(cls, id):
        task = Session.get_instance() \
            .query(cls) \
            .get(id)
        return task

    @classmethod
    def update(cls, id, **kwargs):
        updated = Session.get_instance() \
            .query(cls) \
            .filter(cls.id == id) \
            .update(kwargs)
        Session.get_instance().commit()
        return updated

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
            'text': self.text,
            'description': self.description,
            'expected_data': dump_datetime(self.expected_date),
            'status_id': self.status_id,
        }

    # @property
    # def serialize_many2many(self):
    #     # return [item.serialize for item in self.status]

    def __repr__(self):
        return self.description
