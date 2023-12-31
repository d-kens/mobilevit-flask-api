import os
from decouple import config
from datetime import timedelta

BASE_DIR=os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY=config('SECRET_KEY', 'secret')
    SQLALCHEMY_TRACK_MODIFICATION=False
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=5)
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(minutes=20)
    JWT_SECRET_KEY=config('JWT_SECRET_KEY')

class DevConfig(Config):
    DEBUG=config('FLASK_DEBUG', cast=bool)
    SQLALCHEMY_ECHO=True
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(BASE_DIR, 'db.sqlite3')


class TestConfig(Config):
    pass

class ProdConfig(Config):
    pass


config_dict = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'test': TestConfig
}