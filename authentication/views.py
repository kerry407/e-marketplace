from rest_framework import generics, permissions
# Create your views here.

from .serializers import UserRegistrationSerializer
from utils.renderers import CustomRenderer


class AccountCreateView(generics.CreateAPIView):
    '''
        API endpoint for creating a customer account 
    '''
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    renderer_classes = [CustomRenderer]
