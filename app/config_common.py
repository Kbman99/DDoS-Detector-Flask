import os
import logging

TIMEZONE = 'US/Eastern'

# Secret key for generating tokens
SECRET_KEY = 'houdini'

# Admin credentials
ADMIN_CREDENTIALS = ('admin', 'pa$$word')

# Database choice
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Configuration of a Gmail account for sending mails
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'twitterplaymethis'
MAIL_PASSWORD = 'cassie96'
ADMINS = ['twitterplaymethis@gmail.com']

# Number of times a password is hashed
BCRYPT_LOG_ROUNDS = 12

WEBHOOK_VERIFY_TOKEN = os.getenv('WEBHOOK_VERIFY_TOKEN')
CLIENT_AUTH_TIMEOUT = 9999 # in Hours

LOG_LEVEL = logging.INFO
LOG_FILENAME = 'activity.log'