from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

class RegisterDeviceForm(FlaskForm):

    serial_numer = StringField('Please enter the serial number:')
    submit = SubmitField('Register Device!')

class UnregisterDeviceForm(FlaskForm):

    serial_numer = StringField('Please enter the serial number:')
    submit = SubmitField('Unregister Device!')
