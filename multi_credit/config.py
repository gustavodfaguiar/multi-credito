from decouple import config


class Config(object):
    DEBUG = config('DEBUG', default=False, cast=bool)
    SECRET_KEY = config('SECRET_KEY')
    DEFAULT_DATABASE = 'sqlite:///multi_credit.db'
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URL', default=DEFAULT_DATABASE)


class ProductionConfig(Config):
    DEBUG = config('DEBUG', default=False, cast=bool)


class DevelopmentConfig(Config):
    DEBUG = config('DEBUG', default=False, cast=bool)
    DEFAULT_DATABASE = 'sqlite:///multi_credit.db'
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URL', default=DEFAULT_DATABASE)


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    DEBUG = config('DEBUG', default=False, cast=bool)
    TESTING = True
