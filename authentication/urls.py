from django.urls import path 
from .views import (
    AccountCreateView
)

urlpatterns = [
    path('sign-up/', AccountCreateView.as_view(), name='create-account')
]
