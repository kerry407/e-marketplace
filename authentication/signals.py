from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from utils.helpers import UserRelatedHelper

@receiver(post_save, sender=get_user_model(), dispatch_uid='unique_identifier')
def send_confirmation_email(sender, instance, created, **kwargs) -> None:
    if created:
        subject = "Confirm your email address"
        message = render_to_string('authentication/email_confirmation.html', {
            'user': instance,
            'domain': '127.0.0.1:8000',
            'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
            'token': default_token_generator.make_token(instance)
        })
        helper = UserRelatedHelper(instance)
        helper.send_mail_helper('Confirmation', subject, message)