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
import os

def create_app(config=config_dict['dev']):
    app=Flask(__name__, static_folder=os.path.abspath('api/uploads/'), static_url_path='/api/uploads')

    app.config.from_object(config)

    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)

    api = Api(app)

    register_blueprints(app, api)

    
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'ClassificationResult': ClassificationResult
        }

    return app


def register_blueprints(app, api):
    
    from .auth.views import auth_namespace
    from .classification.views import classification_namespace


    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(classification_namespace, path='/classification')

