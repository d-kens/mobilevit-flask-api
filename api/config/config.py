import os
from decouple import config

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class Config:
    SECRET_KEY = config('SECRET_KEY', default='secret')


class DevConfig(Config):
    DEBUG = config('FLASK_DEBUG', cast=bool, default=True)


class TestConfig(Config):
    pass


class ProdConfig(Config):
    pass


config_dict = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'test': TestConfig
}
