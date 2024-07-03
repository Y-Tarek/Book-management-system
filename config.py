import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://username:password@localhost:5432/books_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-string")
    DEBUG = os.getenv("FLASK_DEBUG",True)


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL","sqlite:///:memory:")
