from django.urls import path 
from .views import (
    AccountCreateView,
    ConfirmEmailView,
    CustomTokenObtainPairView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('sign-up/', AccountCreateView.as_view(), name='create-account'),
    path('confirm-email/<uidb64>/<str:token>/', ConfirmEmailView.as_view(), name='confirm-email'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path("login/refresh/", TokenRefreshView.as_view(), name='token_refresh'),  
]
