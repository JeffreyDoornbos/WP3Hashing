from flask import *
from flasgger import Swagger
from controllers import *
from pathlib import Path

from utils import create_default_env
from utils import load_env


class App:
    __app: Flask
    __swagger: Swagger

    def __init__(self):
        self.__app = Flask(__name__)
        ENV_PATH = Path('./').parent.resolve() / '.env'

        # Check if .env file exists else create with defaults
        if not ENV_PATH.exists():
            create_default_env(ENV_PATH)
            print(f"Created default .env file at {ENV_PATH}")

        self.__app.config.update(load_env(str(ENV_PATH)))
        self.__app.config["SWAGGER"] = {'title': "Accessibility API", 'version': "1.0.0"}

    def add_routes(self):
        config = self.__app.config 
        HomeController(config).add_routes(self.__app)
        UsersController(config).add_routes(self.__app) 
        BeheerdersController(config).add_routes(self.__app)
        APIController(config).add_routes(self.__app)
        ErrorController(config).add_routes(self.__app)
        ErvaringsdeskundigeController(config).add_routes(self.__app)

    def run(self, debug:bool=False):
        #Pre-run values
        self.add_routes()
        self.__swagger = Swagger(self.__app)
        self.__app.run(debug=debug)

if __name__ == '__main__':
    app = App()
    app.run(debug=True)