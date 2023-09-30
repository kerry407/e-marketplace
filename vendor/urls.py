from django.urls import path 
from .views import (
    VendorAPIViewset,
    StoreAPIViewSet
)


urlpatterns = [
    path('create-vendor/', VendorAPIViewset.as_view({'post': 'create'}), name='create-vendor'),
    path('vendors-list/', VendorAPIViewset.as_view({'get': 'list'}), name='vendors-list'),
    path('vendor-profile/<str:pk>/', 
        VendorAPIViewset.as_view(
            {
            'get':'retrieve', 'put':'update', 
            'patch':'partial_update', 
            'delete':'destroy'
            }), 
        name='vendor-detail'
        ),
    path('create-store/', StoreAPIViewSet.as_view({'post':'create'}), name='create-store'),
    path('store-list/', StoreAPIViewSet.as_view({'get': 'list'}), name='store-list'),
    path('store/<str:pk>/', 
        StoreAPIViewSet.as_view(
            {
            'get':'retrieve', 'put':'update', 
            'patch':'partial_update', 
            'delete':'destroy'
            }), 
        name='store-detail'
        ),
]   