from flask import Flask
from flask_restx import Api
from .config.config import config_dict
from flask_cors import CORS


def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    app.config.from_object(config)

    CORS(app)
    api = Api(app)

    from .classification.views import classification_namespace
    api.add_namespace(classification_namespace, path='/classification')

    return app
