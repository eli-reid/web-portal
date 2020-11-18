from wtforms.fields.simple import HiddenField
from .._form_imports import *

class New_Password(FlaskForm):
    """description of class"""
    password = PasswordField('New Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm =  PasswordField('Confirm Password')
    recaptcha = RecaptchaField()