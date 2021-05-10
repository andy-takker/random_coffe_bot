from environs import Env
import os

env = Env()
env.read_env()

basedir = os.path.abspath(os.path.dirname(__file__))

POSTGRES_USER = env.str('POSTGRES_USER')
POSTGRES_PASSWORD = env.str('POSTGRES_PASSWORD')
POSTGRES_DB = env.str('POSTGRES_DB')
POSTGRES_HOST = env.str('POSTGRES_HOST')
SQLALCHEMY_DATABASE_URI = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}'

TELEGRAM_BOT_TOKEN = env.str('TELEGRAM_BOT_TOKEN')
ADMINS = env.list('ADMINS')
