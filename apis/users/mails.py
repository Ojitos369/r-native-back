from app.core.bases.correos import EmailSend, EmailTextSend


class CorreoActivacion(EmailTextSend):
    def __init__(self, *args, **kargs):
        self.to_email = ["ojitos369@gmail.com"]
        self.bcc_email = []
        self.email_subject = "Codigo de Activacion de cuenta"
        self.email_text = "Text"
        
        for k, v in kargs.items():
            setattr(self, k, v)

        if type(self.to_email) == str:
            self.to_email = [self.to_email]
        if type(self.bcc_email) == str:
            self.bcc_email = [self.bcc_email]
