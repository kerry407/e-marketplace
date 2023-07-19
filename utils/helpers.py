from django.core.mail import EmailMessage 
from django.conf import settings
from authentication.models import CustomUser
from typing import List

class UserRelatedHelper:
    
    def __init__(self, instance: CustomUser) -> None:
        self.instance = instance 
        
    def send_mail_helper(self, type: str, subject: str, 
                         message: str, fail_silently: bool=False
                        ) -> None:

        try:
            mail_message = EmailMessage(
                                        subject=subject, body=message, 
                                        from_email=settings.DEFAULT_FROM_MAIL, 
                                        to=[self.instance.email]
                                       )
            mail_message.content_subtype = 'html'
            mail_message.send()
        except Exception as e:
            print(f'Error sending {type} email: {e}')
         