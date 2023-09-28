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
        
    @classmethod 
    def get_file_tuple(cls):
        file_tuple = tuple(f.name for f in cls._meta.get_fields() \
                            if isinstance(cls._meta.get_field(f.name), models.FileField)
                            )
        return file_tuple
    
    def save(self, *args, **kwargs):
        if self.profile_img_url and self.identity:
            # compress profile_img
            self.profile_img_url, self.identity = tuple(image_upload([self.profile_img_url, self.identity]))

        """Deletes former profile_img or identity when making an update to profile_img or identity
        """
        former = Vendor.objects.get(pk=self.user)
        UserRelatedHelper(former).remove_duplicate(self.get_file_tuple(), self)
                    
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.user.first_name
    
    

class Store(TrackObjectStateMixin):
    owner = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='store')
    about = models.CharField(max_length=250)
    
    
