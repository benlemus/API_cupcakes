from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import Optional, URL

class NewCupcakeForm(FlaskForm):
    flavor = StringField('Flavor')

    size = StringField('Size')

    rating = FloatField('Rating')

    image = StringField('Image', validators=[Optional(), URL()])