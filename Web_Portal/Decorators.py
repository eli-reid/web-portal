from functools import wraps

from flask import redirect
from flask import url_for
from flask import session 

from .models import User
 
def LoginRequired(view):
        @wraps(view)
        def decorator(*args, **kwargs):
            if session.get('username'):
                return view(*args, **kwargs)
            return redirect(url_for('home'))
        return decorator


def AdminRequired(view):
    @wraps(view)
    def decorator(*args, **kwargs):
        if session.get('admin'):
            return view(*args, **kwargs)
        return redirect(url_for('home'))                
    return decorator
