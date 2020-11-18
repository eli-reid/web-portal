from .._form_imports import *

class Change_Password(FlaskForm):
    """description of class"""
    current= PasswordField('Current Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm =  PasswordField('Confirm Password')
    recaptcha = RecaptchaField()