import os
from decouple import config
from datetime import timedelta

BASE_DIR=os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY=config('SECRET_KEY', 'secret')
    """
      configures security for the application
    """
    

    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(minutes=30)
    JWT_SECRET_KEY=config('JWT_SECRET_KEY')

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI= 'postgresql://afran:123@localhost:5432/db'
    SQLALCHEMY_TRACK_MODIFICATION=False
    DEBUG=True
    SQLALCHEMY_ECHO=True

class TestConfig(Config):
    TESTING=True

class ProdConfig(Config):
    pass


config_dict={
    'dev':DevConfig,
    'prod':ProdConfig,
    'test':TestConfig
}