from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

class Nameform(FlaskForm):
    name=StringField('username',validators=['DataRequired'])
    submit=SubmitField('Submit',validators=['DataRequired']) 