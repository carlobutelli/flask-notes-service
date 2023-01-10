import os


class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'this-really-needs-to-be-changed')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER = {
        "swagger_version": "2.0",
        "title": "FIT - Flask Init Template",
        "headers": [
            ("Access-Control-Allow-Origin", '*'),
            ("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS"),
            ("Access-Control-Allow-Credentials", "true"),
        ]
    }
    MONGODB_DATABASE_HOST = os.environ.get("MONGODB_DATABASE_HOST")
    MONGODB_USER = os.environ.get("MONGODB_USER")
    MONGODB_USER_PASSWORD = os.environ.get("MONGODB_USER_PASSWORD")
    MONGODB_DATABASE = os.environ.get('MONGODB_DATABASE')


class LocalConfig(BaseConfig):
    """Development configuration"""
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://loki:d0nt4get@localhost:5432/notes')


class TestingConfig(BaseConfig):
    """Test environment configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL', 'sqlite:///test.db')


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://loki:d0nt4get@localhost:5432/notes')


class ProductionConfig(BaseConfig):
    """Production configuration"""
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
