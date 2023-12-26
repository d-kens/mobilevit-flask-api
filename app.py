from flask import Flask
from extentions import db
from image_classification import classification_blueprint

def create_app():
    app = Flask(__name__)

    app.config.from_prefixed_env()

    # initialize extensions
    db.init_app(app)

    # register blueprints
    app.register_blueprint(classification_blueprint, url_prefix="/image_classification")

    return app

