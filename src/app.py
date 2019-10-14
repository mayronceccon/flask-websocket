from flask import Flask
from flask_cors import CORS


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
            app.url_map.strict_slashes = False
            app.config['SECRET_KEY'] = 'secret!'
            CORS(app)
            App.__instance = app
