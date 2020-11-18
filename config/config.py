import email
from os import terminal_size
import secrets
import os

class DB_Config:
    SQLALCHEMY_DATABASE_URI =  "mysql+pymysql://@localhost"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_BINDS = {
            "auth" : "mysql+pymysql:///auth",
            "meetings" : "mysql+pymysql:///meetings"
    }

class DEV_DB_Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///"
    SQLALCHEMY_BINDS = {"auth" : "sqlite:///auth.db",
                        "meetings" : "sqlite:///meetings.db"
                        }


class Form_Config:

    RECAPTCHA_USE_SSL = True
    RECAPTCHA_PRIVATE_KEY = ''
    RECAPTCHA_PUBLIC_KEY = ''
    RECAPTCHA_OPTIONS = { "theme": "white" }


class FileUpload_Config:
    UPLOAD_FOLDER = f"files"
    ALLOWED_EXTENSIONS_DOCS = ".txt, .pdf"
    ALLOWED_EXTENSIONS_VIDEO = ".mp4"

class Email_Config:
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

class BaseConfig:

    SECRET_KEY = ''
    os.environ["SECRET_KEY"]= SECRET_KEY
    SESSION_COOKIE_NAME = "sesions"
    PWD_TOKEN_EXPIRE = 500


class Development_Config(DEV_DB_Config,
                         Form_Config,
                         BaseConfig,
                         FileUpload_Config,
                         Email_Config):
    SECRET_KEY = 'DEV'
    os.environ["SECRET_KEY"]= SECRET_KEY
    pass


class Production_Config(DB_Config,
                        Form_Config,
                        BaseConfig,
                        FileUpload_Config,
                        Email_Config):
    pass