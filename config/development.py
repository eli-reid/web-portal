import email
from os import terminal_size
import secrets
import os

######################################
#           Database Config          #
######################################

SQLALCHEMY_DATABASE_URI = "sqlite:///"
SQLALCHEMY_BINDS = {"auth" : "sqlite:///auth.db",
                    "meetings" : "sqlite:///meetings.db"
                    }
SQLALCHEMY_TRACK_MODIFICATIONS = True

######################################
#           RECAPTCHA Config         #
######################################
RECAPTCHA_USE_SSL = True
RECAPTCHA_PRIVATE_KEY = ''
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_OPTIONS = { "theme": "white" }

######################################
#          File Uplaod Config        #
######################################

UPLOAD_FOLDER = f"files"
ALLOWED_EXTENSIONS_DOCS = ".txt, .pdf"
ALLOWED_EXTENSIONS_VIDEO = ".mp4"

######################################
#          File Uplaod Config        #
######################################

MAIL_SERVER = ''
MAIL_PORT = 465
#MAIL_USE_TLS = True
MAIL_USE_SSL = True
#MAIL_DEBUG = ''
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_DEFAULT_SENDER = ''
#MAIL_MAX_EMAILS = ''
#MAIL_SUPPRESS_SEND = ''
#MAIL_ASCII_ATTACHMENTS = ''


######################################
#          App settings Config        #
######################################
SECRET_KEY = ''
os.environ["SECRET_KEY"]= SECRET_KEY
SESSION_COOKIE_NAME = "sesions"
PWD_TOKEN_EXPIRE = 500
