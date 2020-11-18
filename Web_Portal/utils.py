import os
import jwt 

from datetime import datetime
from flask import session
from flask import current_app as app
from werkzeug.utils import secure_filename
from logging import error
from time import time
from . import db
from .models import User
from .models import Profile

def db_init():
  
    db.create_all()
    user = User()
    user.profile = Profile()
    user.username='admin'
    user.password='admin'
    user.email=f'admin'
    user.created=datetime.now()
    user.profile.first_name='admin' 
    user.profile.last_name='admin' 
    user.profile.address1='na'
    user.profile.city='ll'
    user.profile.state='hh'
    user.profile.zip ='00232'
    user.verified = True
    user.admin = True
    user.add()
        
def valid_login(user):
    user=User(username=user).get_user()
    if user.verify_login():
        session['username'] = user.username
        session['login_key'] = user.login_key
        return True
    return False

#### file utilities ####
class file_utils:

    @staticmethod   
    def upload_file(path, file)-> str:
        # make directory
        try:
            os.mkdir(path)
        except:
            pass
        # check filename   
        filename = secure_filename(file.filename)
        if os.path.isfile(os.path.join(path, filename)):
            filename = file_utils.rename_file(path, filename)
        # save file 
        file.save(os.path.join(path, filename))
        return filename

    @staticmethod  
    def delete_file(path, file)-> None:
        if os.path.exists(os.path.join(path, file)):
            os.remove(os.path.join(path, file))
        # delete directory if emtpy           
        if os.path.exists(path) and len(os.listdir(path)) == 0:
            os.rmdir(path)
        return

    @staticmethod  
    def move_file(prev_path, path, filename)-> str:
        try:
            os.mkdir(path)
        except:
            pass
        new_filename = None
        prev_file_loc = os.path.join(prev_path, filename)
        new_file_loc = os.path.join(path, filename)
            # check file to move exists
        if os.path.isfile(prev_file_loc):
            new_filename = filename
            # rename file if duplicate in new path
            if os.path.isfile(new_file_loc):
                new_filename = file_utils.rename_file(path, filename)
            # move file         
            os.rename(os.path.join(prev_path, filename), os.path.join(path, new_filename))

        # delete directorey if emtpy           
        if os.path.exists(prev_path) and len(os.listdir(prev_path)) == 0:
            os.rmdir(prev_path)
        return new_filename
        
    @staticmethod  
    def rename_file(path, filename)-> str:
        for i in range(1000):
            new_filename = filename.replace('.', f'_{i}.')
            if not os.path.isfile(os.path.join(path, new_filename)):
                return new_filename

##### token Utilities ####
def generate_token(payload: dict, expires: int=500):
    payload['exp'] = time() + payload.get('exp', expires)
    try:
        token = jwt.encode(payload, key=os.getenv('SECRET_KEY'))
    except Exception as e:
        error(e)
        return Exception
    return token.decode('utf-8')

def decode_token(token):
    decoded = jwt.decode(token, key=os.getenv('SECRET_KEY'))
    
