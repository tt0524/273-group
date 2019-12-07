from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

class AddForm(FlaskForm):

    name = StringField('Please enter the name of coffee:')
    submit = SubmitField('Add to menu')
