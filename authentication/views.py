from rest_framework import generics, permissions, views, status
from rest_framework.response import Response
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.

from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer
from utils.renderers import CustomRenderer


class AccountCreateView(generics.CreateAPIView):
    '''
        API endpoint for creating a customer account 
    '''
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    renderer_classes = [CustomRenderer]
    

class ConfirmEmailView(views.APIView):
    renderer_classes = [CustomRenderer]
    
    def get(self, request, uidb64, token):
        
        try: 
            uid = smart_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            return Response({"error": "Invalid user ID"}, status=400)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()
            return Response({"message": "Email confirmation successful"})
        else:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    renderer_classes = [CustomRenderer]