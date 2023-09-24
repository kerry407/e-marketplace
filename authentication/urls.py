from django.urls import path, include
from .views import (
    AccountCreateView,
    ConfirmEmailView,
    CustomTokenObtainPairView,
    ChangePasswordConfirmView,  
    ForgotPasswordRequestTokenViewSet,
    # VendorCreateView
)
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from django_rest_passwordreset.views import (
    ResetPasswordValidateTokenViewSet, 
    ResetPasswordRequestTokenViewSet,
    ResetPasswordConfirmViewSet,
)

app_name = "authentication"

router = DefaultRouter()
router.register(
    r'reset-password/validate_token',
    ResetPasswordValidateTokenViewSet,
    basename='reset-password-validate'
)
router.register(
    r'reset-password',
    ResetPasswordRequestTokenViewSet,
    basename='reset-password-request'
)
router.register(
    r'forgot-password',
    ForgotPasswordRequestTokenViewSet,
    basename='forgot-password-request'
)



urlpatterns = [
    # router viewsets urls
    path("", include(router.urls)),
    
    # regular urls
    path('sign-up/', AccountCreateView.as_view(), name='create-account'),
    path('confirm-email/<uidb64>/<str:token>/', ConfirmEmailView.as_view(), name='confirm-email'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('reset-password/confirm/', ChangePasswordConfirmView.as_view(), name='reset-password-confirm'),
    path('forgot-password/confirm', ResetPasswordConfirmViewSet.as_view({'post': 'create'}), name='forgot-password-confirm'),
    # path('create-vendor/', VendorCreateView.as_view(), name='create-vendor')
]
