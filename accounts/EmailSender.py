from django.core.mail import EmailMessage
from django.conf import settings

import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Emailer:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], 
            body=data['email_body'], 
            from_email= settings.EMAIL_HOST_USER,
            to=[data['to_email']]
            )

        #to the mail on a threading without blocking the main thread
        EmailThread(email).start()