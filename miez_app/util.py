from flask import url_for
from miez_app import app,mail
import os
import secrets
from PIL import Image
from flask_mail import Message



"""Giving a Usermixin structure to the mongodb str data to work with login manager"""




def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def send_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset Email', recipients=[user['email']],sender='support@myhbsconline.com',body= f'''Kindly click on this link
        {url_for('users.reset_token', token=token, _external=True)}
        to reset your password''')

    mail.send(msg)










            