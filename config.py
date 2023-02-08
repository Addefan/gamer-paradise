import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret')
    DEBUG = os.environ.get('DEBUG', True)

    POSTGRES_DB = os.environ.get('POSTGRES_DB', 'postgres')
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT', 5432)
    POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
    POSTGRES_PASS = os.environ.get('POSTGRES_PASS', 'postgres')

    SQLALCHEMY_DATABASE_URI = (f'postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@'
                               f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}')
