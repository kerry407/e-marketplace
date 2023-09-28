from django.urls import path 
from .views import (
    VendorAPIViewset
)


urlpatterns = [
    path('create-vendor/', VendorAPIViewset.as_view({'post': 'create'}), name='create-vendor'),
    path('vendors-list/', VendorAPIViewset.as_view({'get': 'list'}), name='vendors-list'),
    path('<str:pk>/', 
        VendorAPIViewset.as_view(
            {
            'get':'retrieve', 'put':'update', 
            'patch':'partial_update', 
            'delete':'destroy'
            }), 
        name='vendor-detail'
        ),
]