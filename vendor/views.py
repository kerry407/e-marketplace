from rest_framework import generics, permissions, viewsets, validators
from django_auto_prefetching import AutoPrefetchViewSetMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

# Create your views here.
from common.renderers import CustomRenderer 
from common import permissions as custom_permissions
from .serializers import VendorSerializer, StoreSerializer
from .models import Vendor, Store


class VendorAPIViewset(AutoPrefetchViewSetMixin, viewsets.ModelViewSet):
    # set defaults
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer 
    renderer_classes = [CustomRenderer]
    parser_classes = [MultiPartParser, FormParser]
    
    
    def get_queryset(self):
        # define queryset for staff and normal users
        
        if self.request.user.is_staff:
            return super().get_queryset()
        return super().get_queryset().filter(user__is_active=True)
    
    def get_permissions(self):
        # define permissions based on the action a user wants to perform
        
        if self.action == 'create':
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'partial_update']:
            self.permission_classes = [custom_permissions.IsOwnerOrReadOnly]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise validators.ValidationError(
                                            {
                                            "detail": "This user already has a Vendor Profile"
                                            }
                                            )
            
        
class StoreAPIViewSet(AutoPrefetchViewSetMixin, viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer 
    renderer_classes = [CustomRenderer]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_queryset(self):
        # define queryset for staff and normal users
        
        if self.request.user.is_staff:
            return super().get_queryset()   
        return super().get_queryset().filter(owner__user__is_active=True) 
    
    def get_permissions(self):
        # define permissions based on the action a user wants to perform
        
        if self.action == 'create':
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'partial_update']:
            self.permission_classes = [custom_permissions.IsOwnerOrReadOnly]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()    
    
    
    def perform_create(self, serializer):
        try:
            
            vendor = get_object_or_404(Vendor, user=self.request.user)
            serializer.save(owner=vendor)
        except IntegrityError:
            raise validators.ValidationError(
                                            {
                                            "detail": "A store with this name has already been created."
                                            }
                                            )