from flask import *
from models import Model

class Controller:
    _cfg: Config
    _blueprint: Blueprint
    _model: Model

    def __init__(self, cfg:Config):
        self._cfg = cfg

    @property
    def config(self):
        return self._cfg

    @property
    def blueprint(self):
        return self._blueprint;

    @property
    def model(self):
        return self._model

    def add_routes(self, app:Flask):
        pass