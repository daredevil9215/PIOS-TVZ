from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from app import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body,
               attachments=None, sync=False):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)
    if sync:
        mail.send(msg)
        print("message sent")
    else:
        Thread(target=send_async_email,
               args=(current_app._get_current_object(), msg)).start()


def send_order_successful_email(user, order):
    send_email('[TIM09] Narudžba Uspješna',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/order_successful.txt',
                                         user=user, order=order),
               html_body=render_template('email/order_successful.html',
                                         user=user, order=order))
