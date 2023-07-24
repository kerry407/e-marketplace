from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse


from utils.helpers import UserRelatedHelper, forgot_password_token_created
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(post_save, sender=get_user_model(), dispatch_uid='unique_identifier')
def send_confirmation_email(sender, instance, created, **kwargs) -> None:
    if created:
        subject = "Confirm your email address"
        # render email html
        message = render_to_string('authentication/email_confirmation.html', {
            'user': instance,
            'domain': '127.0.0.1:8000',
            'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
            'token': default_token_generator.make_token(instance)
        })
        helper = UserRelatedHelper(instance)
        helper.mailer('Confirmation', subject, message)
        

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # send an e-mail to the user
    subject = "Reset Password request"
    context = {
        'current_user': reset_password_token.user,
        'first_name': reset_password_token.user.first_name,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
                    instance.request.build_absolute_uri(reverse('authentication:reset-password-confirm')),
                    reset_password_token.key)
        }
    # render email html
    message = render_to_string('authentication/user_reset_password.html', context)
    helper = UserRelatedHelper(reset_password_token.user)
    helper.mailer('Confirmation', subject, message)


@receiver(forgot_password_token_created)
def forgot_password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # send an e-mail to the user
    subject = "Reset Password request"
    context = {
        'current_user': reset_password_token.user,
        'first_name': reset_password_token.user.first_name,
        'email': reset_password_token.user.email,
        'forgot_password_url': "{}?token={}".format(
                    instance.request.build_absolute_uri(reverse('authentication:forgot-password-confirm')),
                    reset_password_token.key)
        }
    print(context['forgot_password_url'])
    # render email html
    message = render_to_string('authentication/user_forgot_password.html', context)
    helper = UserRelatedHelper(reset_password_token.user)
    helper.mailer('Confirmation', subject, message)