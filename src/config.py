import os

class Development(object):
    """
    Development Environment configuration
    """
    DEBUG = True
    TESTING = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY_DEV')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL_DEV')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Production(object):
    """
    Production environment configurations
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

app_config = {
    'development': Development,
    'production': Production,
}
