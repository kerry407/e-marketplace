from django.core.mail import EmailMessage 
from django.conf import settings
from authentication.models import CustomUser
from rest_framework import exceptions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django_rest_passwordreset.views import _unicode_ci_compare
from django_rest_passwordreset.models import ResetPasswordToken, clear_expired, get_password_reset_token_expiry_time, \
    get_password_reset_lookup_field
from django_rest_passwordreset.serializers import EmailSerializer
from django.dispatch import Signal 
from django.core.files.uploadedfile import InMemoryUploadedFile

import threading
from io import BytesIO 
import sys 
import contextlib 
from PIL import Image
from typing import Sequence, Any 

User = get_user_model()

HTTP_USER_AGENT_HEADER = getattr(settings, 'DJANGO_REST_PASSWORDRESET_HTTP_USER_AGENT_HEADER', 'HTTP_USER_AGENT')
HTTP_IP_ADDRESS_HEADER = getattr(settings, 'DJANGO_REST_PASSWORDRESET_IP_ADDRESS_HEADER', 'REMOTE_ADDR')

forgot_password_token_created = Signal()


class EmailThread(threading.Thread):
    
    def __init__(self, email: EmailMessage) -> None:
        self.email = email 
        threading.Thread.__init__(self)
        
    def run(self) -> None:
        try:
            self.email.send()  
        except Exception:
            pass 

class UserRelatedHelper:
    
    def __init__(self, instance: CustomUser) -> None:
        self.instance = instance 
        
    def mailer(self, type: str, subject: str, message: str) -> None:

        try:
            mail_message = EmailMessage(
                                        subject=subject, body=message, 
                                        from_email=settings.DEFAULT_FROM_MAIL, 
                                        to=[self.instance.email]
                                       )
            mail_message.content_subtype = 'html'
            EmailThread(mail_message).start()
        except Exception as e:
            print(f'Error sending {type} email: {e}')
            
            
    def remove_duplicate(self, files: Sequence[Any], klass):
        with contextlib.suppress(Exception):
            for file in files:
                if getattr(self.instance, f'{file}') != getattr(klass, f'{file}'):
                    old_file = getattr(self.instance, f'{file}')
                    print(old_file, getattr(klass, f'{file}'))
                    old_file.delete(save=False)
                    
         
      
class ForgotPasswordRequestToken(GenericAPIView):
    """
    An Api View which provides a method to request a password reset token based on an e-mail address

    Sends a signal reset_password_token_created when a reset token was created
    """
    throttle_classes = ()
    permission_classes = ()
    serializer_class = EmailSerializer
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        # before we continue, delete all existing expired tokens
        password_reset_token_validation_time = get_password_reset_token_expiry_time()

        # datetime.now minus expiry hours
        now_minus_expiry_time = timezone.now() - timedelta(hours=password_reset_token_validation_time)

        # delete all tokens where created_at < now - 24 hours
        clear_expired(now_minus_expiry_time)

        # find a user by email address (case insensitive search)
        users = User.objects.filter(**{'{}__iexact'.format(get_password_reset_lookup_field()): email})

        active_user_found = False

        # iterate over all users and check if there is any user that is active
        # also check whether the password can be changed (is useable), as there could be users that are not allowed
        # to change their password (e.g., LDAP user)
        for user in users:
            if user.eligible_for_reset():
                active_user_found = True
                break

        # No active user found, raise a validation error
        # but not if DJANGO_REST_PASSWORDRESET_NO_INFORMATION_LEAKAGE == True
        if not active_user_found and not getattr(settings, 'DJANGO_REST_PASSWORDRESET_NO_INFORMATION_LEAKAGE', False):
            raise exceptions.ValidationError({
                'email': [_(
                    "We couldn't find an account associated with that email. Please try a different e-mail address.")],
            })

        # last but not least: iterate over all users that are active and can change their password
        # and create a Reset Password Token and send a signal with the created token
        for user in users:
            if user.eligible_for_reset() and \
                    _unicode_ci_compare(email, getattr(user, get_password_reset_lookup_field())):
                # define the token as none for now
                token = None

                # check if the user already has a token
                if user.password_reset_tokens.all().count() > 0:
                    # yes, already has a token, re-use this token
                    token = user.password_reset_tokens.all()[0]
                else:
                    # no token exists, generate a new token
                    token = ResetPasswordToken.objects.create(
                        user=user,
                        user_agent=request.META.get(HTTP_USER_AGENT_HEADER, ''),
                        ip_address=request.META.get(HTTP_IP_ADDRESS_HEADER, ''),
                    )
                # send a signal that the password token was created
                # let whoever receives this signal handle sending the email for the password reset
                forgot_password_token_created.send(sender=self.__class__, instance=self, reset_password_token=token)
        # done
        return Response({'status': 'OK'})


def image_upload(files: list):
    # opening the uploaded image 
    
    for image_file in files:
        im = Image.open(image_file)
        output = BytesIO()
        
        # resize or modify the image to fit aspect ratio
        original_width, original_height = im.size
        aspect_ratio = round(original_width / original_height)
        desired_height = 100  # Edit to add your desired height in pixels
        desired_width = desired_height * aspect_ratio
        im = im.resize((desired_width, desired_height))  # resize the image
        
        # after modification, save it to the output 
        if im.mode in ("RGBA", "P"):
            im = im.convert("RGB")
        im.save(output, format='JPEG', quality=90)
        output.seek(0)
        
        # change the imagefield value to be the newley modifed image value
        image_file = InMemoryUploadedFile(
                                output, 'ImageField', "%s.jpg" % image_file.name.split('.')[0], 
                                'image/jpeg', sys.getsizeof(output), None
                                )
        yield image_file
        
        

class FileCleanMixin:
    
    def optimize(self):
        pass 
    
    
    