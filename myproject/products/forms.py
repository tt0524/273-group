from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField,RadioField
from myproject.models import Product



# choices = [(1, "temp_product")]


class Buy(FlaskForm):

    select_product = RadioField("Select Product", choices=[],coerce=int)
    submit = SubmitField('Purchase!')
