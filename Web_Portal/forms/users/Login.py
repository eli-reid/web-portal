from .._form_imports import * 

class Login(FlaskForm):
    """description of class"""
    username = StringField(u'Username', validators=[DataRequired()], description='Username', id='username')
    password = PasswordField(u'Password',validators=[DataRequired()])
    recaptcha = RecaptchaField()