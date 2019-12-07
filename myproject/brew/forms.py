from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField,RadioField
from myproject.models import Menu, Device
from flask_login import login_required,current_user

# class BrewCoffeeForm(FlaskForm):
#
#     brew_menu = RadioField("Select Menu", choices=[])
#     brew_device = RadioField("Select Devices", choices=[])
#     # working_device = RadioField("Working Devices", choices=select_device, render_kw={'readonly': True, 'disabled':True})
#     submit = SubmitField('Brew Coffee!')
