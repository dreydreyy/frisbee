from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, RadioField
from wtforms.validators import InputRequired, Length, NumberRange

# New type of form with radiofield and selectfield
class JerseyForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=2, max=40)])
    number = IntegerField('Number', validators=[InputRequired(),
                                                NumberRange(1, 99, "Please enter a number between 1 and 99")])
    size = SelectField('Size', choices=[('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')],
                       validators=[InputRequired()])
    type = RadioField('Color', choices=[('white', 'white'), ('red', 'red'), ('both', 'both')],
                      validators=[InputRequired()])
    submit = SubmitField('Post')
