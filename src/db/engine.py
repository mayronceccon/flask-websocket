from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from .base import Base


class Engine:
    __instance = None

    @staticmethod
    def get_instance():
        if Engine.__instance is None:
            Engine()
        return Engine.__instance

    def __init__(self):
        if Engine.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Engine.__instance = create_engine(
                'sqlite:///socket.sqlite',
                connect_args={
                    'check_same_thread': False
                },
                poolclass=StaticPool,
                echo=True
            )
            Base.get_instance().metadata.create_all(Engine.get_instance())
