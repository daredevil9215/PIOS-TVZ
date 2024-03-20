import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 's3cret'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root@127.0.0.1/tim09-dev'
