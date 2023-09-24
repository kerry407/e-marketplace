from rest_framework import generics, permissions, views, status
from rest_framework.response import Response
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.views import TokenObtainPairView
from django_rest_passwordreset.models import ResetPasswordToken
from rest_framework.viewsets import GenericViewSet
from django.core.exceptions import ValidationError
from rest_framework import exceptions
from django.contrib.auth.password_validation import validate_password, get_password_validators
from django.conf import settings
from .permissions import CustomUserPermissions

# Create your views here.

from .serializers import (
    UserRegistrationSerializer, 
    CustomTokenObtainPairSerializer, 
    ChangePasswordSerializer
)
from common.renderers import CustomRenderer
from utils.helpers import ForgotPasswordRequestToken

User = get_user_model()

class AccountCreateView(generics.CreateAPIView):
    '''
        API endpoint for creating a customer account 
    '''
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    renderer_classes = [CustomRenderer]
    

class ConfirmEmailView(views.APIView):
    '''
        API endpoint for confirming email address on account creation
    '''
    renderer_classes = [CustomRenderer]
    
    def get(self, request, uidb64, token):
        
        try: 
            uid = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid user ID"}, status=400)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()
            return Response({"message": "Email confirmation successful"})
        else:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        


class ChangePasswordConfirmView(generics.CreateAPIView):
    '''
        API endpoint for confirming change of user passwords
    '''
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer                                                                                                                                                     
    renderer_classes = [CustomRenderer]
    permission_classes = [CustomUserPermissions]
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = request.data["token"]
        reset_password_queryset = ResetPasswordToken.objects.filter(key=token)
        reset_password_token_exists = reset_password_queryset.exists()
        if not reset_password_token_exists:
            raise exceptions.ValidationError({
                "error": "Invalid token"
            })
        reset_password_token = reset_password_queryset.first()
            
        # check if former password is correct
        old_password = request.data["old_password"]
        if not reset_password_token.user.check_password(old_password):
            return Response({"error": "Incorrect old password"}, status=status.HTTP_400_BAD_REQUEST)
        
        new_password = request.data["new_password"]
        
        try:
            # validate the password against existing validators
            validate_password(
                new_password,
                user=reset_password_token.user,
                password_validators=get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)
            )
        except ValidationError as e:
            # raise a validation error for the serializer
            raise exceptions.ValidationError({
                'password': e.messages
            })
        reset_password_token.user.set_password(new_password)
        reset_password_token.user.save()
        
        # Delete all password reset tokens for this user
        ResetPasswordToken.objects.filter(user=reset_password_token.user).delete()
        
        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
    
    

class ForgotPasswordRequestTokenViewSet(ForgotPasswordRequestToken, GenericViewSet):
    """
    An Api ViewSet which provides a method to request a password reset token based on an e-mail address

    Sends a signal reset_password_token_created when a reset token was created
    """

    def create(self, request, *args, **kwargs):
        return super(ForgotPasswordRequestTokenViewSet, self).post(request, *args, **kwargs)
    

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    renderer_classes = [CustomRenderer]
    
    

    