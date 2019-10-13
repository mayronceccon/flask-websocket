from flask import Flask
from flask_socketio import SocketIO
from .app import App


class Socketio:
    __instance = None

    @staticmethod
    def get_instance():
        if Socketio.__instance is None:
            Socketio()
        return Socketio.__instance

    def __init__(self):
        if Socketio.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            async_mode = None
            Socketio.__instance = SocketIO(
                App.get_instance(),
                async_mode=async_mode
            )
