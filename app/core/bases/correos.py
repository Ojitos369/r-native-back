
# from email.MIMEText import MIMEText
from django.core.mail import EmailMultiAlternatives, EmailMessage
from ojitos369.utils import get_d
from app.settings import email_settings, prod_mode

DEFAULT_FROM_EMAIL = email_settings["sender"]
class EmailSend:
    def send(self):
        from_email = DEFAULT_FROM_EMAIL
        to_email = self.to_email if prod_mode else ['ojitos369@gmail.com']
        if hasattr(self, 'bcc_email'):
            bcc_email = self.bcc_email
        else:
            bcc_email = []
        bcc_email = bcc_email if prod_mode else []

        email_html = self.email_html
        email_message = EmailMultiAlternatives(
            subject = self.email_subject,
            body = email_html,
            from_email = from_email,
            to = to_email,
            bcc = bcc_email,
        )
        email_message.attach_alternative(email_html, 'text/html')
        # verify if self has file_names attribute
        if hasattr(self, 'file_names'):
            for file_name in self.file_names:
                with open(f'{self.rute_file}/{file_name[0]}', 'rb') as f:
                    email_message.attach(file_name[0], f.read(), file_name[1])
        email_message.send()
        # if connection: connection.close()
        return True


class EmailTextSend:
    def send(self):
        from_email = DEFAULT_FROM_EMAIL
        to_email = self.to_email if prod_mode else ['ojitos369@gmail.com']
        if hasattr(self, 'bcc_email'):
            bcc_email = self.bcc_email
        else:
            bcc_email = []
        bcc_email = bcc_email if prod_mode else []
        
        email_message = EmailMessage(
            subject = self.email_subject,
            body = self.email_text,
            from_email = from_email,
            to = to_email,
            bcc = bcc_email
        )
        
        if hasattr(self, 'file_names'):
            for file_name in self.file_names:
                with open(f'{self.rute_file}/{file_name[0]}', 'rb') as f:
                    email_message.attach(file_name[0], f.read(), file_name[1])
        email_message.send()
        return True


class BaseText(EmailTextSend):
    def __init__(self, *args, **kargs):
        self.to_email = ["ojitos369@gmail.com"]
        self.bcc_email = []
        self.email_subject = "Subject"
        self.email_text = "Text"
        
        for k, v in kargs.items():
            setattr(self, k, v)

        if type(self.to_email) == str:
            self.to_email = [self.to_email]
        if type(self.bcc_email) == str:
            self.bcc_email = [self.bcc_email]


class BaseHtml(EmailSend):
    def __init__(self, *args, **kargs):
        self.to_email = ["ojitos369@gmail.com"]
        self.bcc_email = []
        self.email_subject = "Subject"
        self.email_html = "<h1>Html</h1>"
        
        for k, v in kargs.items():
            setattr(self, k, v)

        if type(self.to_email) == str:
            self.to_email = [self.to_email]
        if type(self.bcc_email) == str:
            self.bcc_email = [self.bcc_email]
