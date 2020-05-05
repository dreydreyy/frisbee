from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from website.models import User

# Registration form which is a normal Flaskform with normal registration fields and validators
class RegistrationForm(FlaskForm) :
    username=StringField('Username', validators=[InputRequired(), Length(min=3, max=30)])
    email = EmailField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=3, max=30)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken, please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken, please choose a different one.')


# Login form which is a normal Flaskform with normal email and password login field and normal validators
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


# same form as the registration form but without the password and with a picture field which has a file
# extension validator who only accepts jpg and png extensions
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


# simple form which takes in a username and checks if it exists in the database
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


# simple reset password form which modifies the user's password in the database
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')