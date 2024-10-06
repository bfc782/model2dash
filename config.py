import os

basedir = os.path.abspath(os.path.dirname(__file__))
app_name = basedir.split('/')[-2]

MODELS_TO_LOAD = ['User', 'Team']


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = app_name.title()
    MAIL_SENDER = f'{app_name.title()} Admin <{app_name.lower()}@example.com>'
    ADMIN = os.environ.get(f'{app_name.upper()}_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MODELS_TO_LOAD = MODELS_TO_LOAD

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(app_name, 'data-dev.sqlite')

    SQLALCHEMY_DATABASE_URI = "sqlite:///intendif.db"

class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
    #     'sqlite://'

    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/intendif"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(app_name, 'data.sqlite')
    

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}