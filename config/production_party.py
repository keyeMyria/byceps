# an examplary configuration file of a public party web application to
# be run in production

from pathlib import Path


MAX_CONTENT_LENGTH = 4000000
PROPAGATE_EXCEPTIONS = True

# Set a custom secret key for running in production!
# To generate one:
#     $ python -c 'import os; print(os.urandom(24))'
SECRET_KEY = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

SESSION_COOKIE_SECURE = True

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://byceps:boioioing@127.0.0.1/byceps'

REDIS_URL = 'unix:///var/run/redis/redis.sock?db=0'

MODE = 'public'
BRAND = 'example-brand'
PARTY = 'example-party-1'

PATH_DATA = Path('./data')
PATH_GLOBAL = PATH_DATA / 'global'
PATH_BRAND = PATH_DATA / 'brands' / BRAND
PATH_PARTY = PATH_DATA / 'parties' / PARTY
PATH_USER_AVATAR_IMAGES = PATH_GLOBAL / 'users/avatars'

MAIL_DEBUG = False
MAIL_DEFAULT_SENDER = 'BYCEPS <noreply@example.com>'
MAIL_SUPPRESS_SEND = False
