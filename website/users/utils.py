import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from website import mail

# this file is for functions that are used in the routes page, this file exists so the route page isn't
# too filled with external stuff


# since only image links are saved in the database, we need to save the actual profile pictures in a
# sub folder in the data folder, however, to make sure 2 pictures aren't saved on the same name, we
# generate a random hex token for each picture replacing their actual name, we also save the picture
# being already cropped to the desired size so they don't take too much memory space
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


# Sends an email to the user's email with a link for resetting password. The sender will appear as no-reply
# but it is really the email we put in the configuration. Will redirect to the password reset page upon
# clicking the link and will also sen the token to that page who will check its validity
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)
