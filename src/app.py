from flask import Flask


class App:
    __instance = None

    @staticmethod
    def get_instance():
        if App.__instance is None:
            App()
        return App.__instance

    def __init__(self):
        if App.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            app = Flask(__name__)
            app.config['SECRET_KEY'] = 'secret!'
            App.__instance = app
