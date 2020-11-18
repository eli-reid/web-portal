from .._form_imports import *
from .States import states
class Edit(FlaskForm):
    """description of class"""
    email =  EmailField('Email', validators=[DataRequired(), Email(message='Enter Vialid Email!')])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    address1 = StringField('Address 1', validators=[DataRequired()])
    address2 = StringField('Address 2')
    city = StringField('City', validators=[DataRequired()])
    state = SelectField('State', choices=[(state['abbr'], state['name']) for state in states])
    zip = StringField('Zip', validators=[DataRequired()])
    home_phone = TelField('Home Phone:', validators=[DataRequired()])
    mobile_phone = TelField('Mobile Phone:')
  