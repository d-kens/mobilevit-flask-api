from flask import Flask
from flask_restx import Api
from .auth.views import auth_namespace
from .classification.views import classification_namespace
from .config.config import config_dict
from .utils import db
from .models.users import User
from .models.classification_results import ClassificationResult
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

def create_app(config=config_dict['dev']):
    app=Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    jwt = JWTManager(app)

    api = Api(app) # This line creates a Flask-RESTx API instance associated with the Flask application app

    migrate = Migrate(app, db)

    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(classification_namespace, path='/classification')

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'ClassificationResult': ClassificationResult
        }


    return app