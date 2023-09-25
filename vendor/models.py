from django.db import models
from django.conf import settings 
import contextlib
from authentication.models import TrackObjectStateMixin

from utils.helpers import image_upload, UserRelatedHelper
# Create your models here.


class Vendor(TrackObjectStateMixin):
    id = None
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    bio = models.TextField()
    profile_img_url = models.ImageField(upload_to='vendors/profile_images/', null=True)
    identity = models.FileField(upload_to='vendors/identities/', null=True)
    
    class Meta:
        unique_together = ("user", "user")
        ordering = ["last_updated"]
    
    def save(self, *args, **kwargs):
        if self.profile_img_url and self.identity:
            # compress profile_img
            self.profile_img_url, self.identity = tuple(image_upload([self.profile_img_url, self.identity]))

        """Deletes old profile_img when making an update to profile_img"""
        old_objects = Vendor.objects.get(user=self.user)
        UserRelatedHelper(old_objects).remove_duplicate([self.profile_img_url, self.identity])
            
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.user.first_name
    
    