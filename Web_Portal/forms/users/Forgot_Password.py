from .._form_imports import * 

class Forgot_Password(FlaskForm):
    """description of class"""
    email = EmailField('Email', validators=[DataRequired(), Email(message='Enter Valid Email!')])
    recaptcha = RecaptchaField()

