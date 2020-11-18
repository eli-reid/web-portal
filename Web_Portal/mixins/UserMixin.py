
from os import SEEK_CUR
import bcrypt
from flask.globals import session
import jwt
from jwt.exceptions import  ExpiredSignatureError, InvalidSignatureError
from ..adapters import SQLDBAdapter
import os
from time import time 
from logging import error

class UserMixin(SQLDBAdapter):
    """description of class"""

    def __init__(self, *args, **kwargs):
        #populate table values
        for key, value in kwargs.items():
            self.__dict__[key] = value
        return super().__init__(*args, **kwargs)

    def __repr__(self):
        return self.username

    def add(self):
        self._hash_password()
        super().add()
        return self

    def update_pw(self):
        self._hash_password()
        self.update()
        return self

    def exists(self):
        return self.get_user() is not None

    def get_user(self):
        self = self.get_first(username=self.username)
        return self 

    def _hash_password(self):
        if self.password is not None:
            self.password = bcrypt.hashpw(self.password.encode(), bcrypt.gensalt(rounds=13))

    def verify_login(self, password):
        if self.exists():
            try:
                return  bcrypt.checkpw(password.encode(), self.password.encode())
            except AttributeError: # catches if the database returns byte code
                return  bcrypt.checkpw(password.encode(), self.password)
        return False

    def get_reset_token(self, expires=500):
        key = os.getenv('SECRET_KEY')
        expires = time() + expires
        try:
            reset_token = jwt.encode({
                                'pw_reset': self.username, 
                                'exp': expires, 
                                'pw': self.password
                                }, key,)
        except TypeError:
            reset_token = jwt.encode({
                                'pw_reset': self.username, 
                                'exp': expires, 
                                'pw': self.password.decode()
                                }, key)
        except Exception as e:
            error(e)
            return self(failed=True, reason_fail = e) 
        return reset_token.decode('utf-8')


    @classmethod
    def verify_reset_token(cls, token):
        user = cls()
        try:
            decoded = jwt.decode(token, key=os.getenv('SECRET_KEY'))
        except InvalidSignatureError:
            return cls(failed=True, reason_fail = "Invalid Token!")
        except ExpiredSignatureError:
            return cls(failed=True, reason_fail = "Token expired!")
        except Exception as e:
            return cls(failed=True, reason_fail = e)
        else:
            user.username = decoded.get('username')
            user.get_user()
            if user.password != decoded.get('pw'):
                return cls(failed=True, reason_fail = "Token already used!")
        return user

    @classmethod
    def populate_form(cls, form):
        for key in cls.__dict__.keys():
            if key in form.data.keys():
                setattr(cls,key,form.data.get(key))
        return cls