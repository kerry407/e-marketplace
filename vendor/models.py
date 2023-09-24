from django.db import models
from django.conf import settings 
import contextlib
from authentication.models import TrackObjectStateMixin

from utils.helpers import image_upload
# Create your models here.


class Vendor(TrackObjectStateMixin):
    id = None
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    bio = models.TextField()
    profile_img_url = models.ImageField(upload_to='uploads/vendors/', null=True)
    identity = models.FileField(null=True)
    
    class Meta:
        unique_together = ("user", "user")
        ordering = ["last_updated"]
    
    def save(self, *args, **kwargs):
        if self.profile_img_url:
            self.profile_img_url = image_upload(self.profile_img_url)
            """Deletes old cover_image when making an update to cover_image"""
            with contextlib.suppress(Exception):
                old = Vendor.objects.get(user=self.user)
                if old.profile_img_url != self.profile_img_url:
                    old.profile_img_url.delete(save=False)
                
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.user.first_name
    
    