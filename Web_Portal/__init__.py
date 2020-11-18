"""
The flask application package.
"""
from config import config
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

mail = Mail()
db = SQLAlchemy()

def create_app(env="production"):

    app = Flask(__name__, instance_relative_config=False)

    if env == "dev":
        app.config.from_object(config.Development_Config)
    else:
        app.config.from_object(config.Production_Config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass    

    # make upload folder
    try:
        os.mkdir(app.config.get('UPLOAD_FOLDER'))
    except OSError:
        pass    

    mail.init_app(app)
   
    # initialize db with app 
    db.init_app(app)
    
    with app.app_context():
        from .routes import home
        from .routes import admin
        from .routes import user
        from .routes import meetings
        return app

