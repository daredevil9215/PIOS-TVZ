import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 's3cret'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root@127.0.0.1/tim09-dev'
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'localhost'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 8025)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['info@tim09.hr']
