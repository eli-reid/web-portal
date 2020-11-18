
from .. import mail
from flask import render_template
from flask_mail import Message
from logging import fatal
from logging import log
from logging import error

class Email:
    @staticmethod
    def send_forgot_password(user)-> bool:
        try:
            key = user.get_reset_token()
            msg: Message = Message()
            msg.subject = "Ever April Password Reset"
            msg.reply_to = 'No-Reply@everapril.org'
            msg.add_recipient(user.email)
            msg.html = render_template('email/reset_pw.html', user=user, key=key)
            mail.send(msg)
            return True
        except Exception as e:
            error(e)
            return False

    
    @staticmethod
    def send_verifaction(user)-> bool:
        try:
            msg: Message = Message()
            msg.subject = "Ever April Email Verifaction"
            msg.reply_to = 'No-Reply@everapril.org'
            msg.add_recipient(user.email)
            msg.html = render_template('email/verify.html', user=user)
            mail.send(msg)
            return True
        except Exception as e:
            error(e)
            return False