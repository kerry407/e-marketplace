from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _ 
from django.conf import settings
from typing import List
# Create your models here.

import uuid
from utils.models import TrackObjectStateMixin
from .manager import CustomUserManager


class CustomUser(AbstractUser, TrackObjectStateMixin):
    
    class GenderOptions(models.TextChoices):
        MALE = "Male", "Male"
        FEMALE = "Female", "Female"
    
    username = None 
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=50) 
    last_name = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False, db_index=True)
    gender = models.CharField(max_length=10, choices=GenderOptions.choices)
    
    USERNAME_FIELD: str = 'email' 
    REQUIRED_FIELDS: List[str] = ["first_name", "last_name"]
    
    objects = CustomUserManager()
    
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_verified = True 
        return super().save(*args, **kwargs)
        
    @property
    def get_user_fullname(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self) -> str:
        return self.get_user_fullname 
    
    
