from flask import *
from controllers import Controller

class ErrorController(Controller):
    def add_routes(self, app):
        return app