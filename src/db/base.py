from sqlalchemy.ext.declarative import declarative_base


class Base:
    __instance = None

    @staticmethod
    def get_instance():
        if Base.__instance is None:
            Base()
        return Base.__instance

    def __init__(self):
        if Base.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Base.__instance = declarative_base()
