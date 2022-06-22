from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.core.mail import send_mail
from django.conf import settings

class Send_Email:

    def __init__(self,template_name,context):
        self.template = get_template(template_name)
        self.content = self.template.render(context)
    
    def Send_Email_Recover(self):
        subject = "Reestrablece tu contraseña"
        message = EmailMultiAlternatives(subject,'',
            settings.EMAIL_HOST_USER,
            ["sellerevansoft@gmail.com"]
        )
        message.attach_alternative(self.content, 'text/html')
        message.send(fail_silently=False)




