# configuration variables for database and email for sending emails to users and also a secret key to protect
# our app from online hackers
import os
import json

# with open('/etc/config.json') as config_file:
#  config = json.load(config_file)


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY_FRISBEE')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
