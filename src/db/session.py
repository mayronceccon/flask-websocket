from sqlalchemy.orm import sessionmaker
from .engine import Engine


class Session:
    __instance = None

    @staticmethod
    def get_instance():
        if Session.__instance is None:
            Session()
        return Session.__instance

    def __init__(self):
        if Session.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            SessionMaker = sessionmaker(bind=Engine.get_instance())
            Session.__instance = SessionMaker()
