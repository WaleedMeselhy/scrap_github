import os

from flask import Flask
from flask_cors import CORS

from .routes import rest_api


def create_app():
    # instantiate the app
    app = Flask(__name__)

    # enable CORS
    CORS(app)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # register blueprints
    app.register_blueprint(rest_api)

    return app
