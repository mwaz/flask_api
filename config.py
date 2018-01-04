"""Configuration file for the app
"""
import os


class Config(object):
    """Parent configuration class
    """
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET', '#%$#%$^FDFGFGdf')
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:@localhost:5432/flask_api'


class DevelopmentConfig(Config):
    """Configurations for Development
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:@localhost:5432/flask_api'


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        'postgresql://postgres:@localhost:5432/test_db')
    DEBUG = True


class StagingConfig(Config):
    """Configurations for Staging
    """
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        'postgresql://postgres:@localhost:5432/flask_api')
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
