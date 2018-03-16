from pathlib import Path


DEBUG = True
SECRET_KEY = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
SESSION_COOKIE_SECURE = False

# SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://byceps:boioioing@127.0.0.1/byceps'
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://byceps:123456@127.0.0.1/byceps'

REDIS_URL = 'redis://127.0.0.1:6379/0'

RQ_DASHBOARD_ENABLED = True

MODE = 'admin'

PATH_DATA = Path('./data')
PATH_GLOBAL = PATH_DATA / 'global'
PATH_USER_AVATAR_IMAGES = PATH_GLOBAL / 'users/avatars'

MAIL_DEBUG = True
MAIL_DEFAULT_SENDER = 'BYCEPS <noreply@example.com>'
MAIL_SUPPRESS_SEND = True

ROOT_REDIRECT_TARGET = 'admin/dashboard'
