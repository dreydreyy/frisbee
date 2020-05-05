from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired


# Normal flaskform with Stringfield and TextArea field and simple validators
class PostForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    content = TextAreaField('Content', validators=[InputRequired()])
    submit = SubmitField('Post')