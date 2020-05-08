from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length


# Normal flaskform with Stringfield and TextArea field and simple validators
class PostForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(min=1, max=100)])
    content = TextAreaField('Content', validators=[InputRequired(), Length(min=1, max=400)])
    submit = SubmitField('Post')