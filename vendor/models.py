from django.db import models
from django.conf import settings 
import contextlib
from authentication.models import TrackObjectStateMixin

from utils.helpers import UserRelatedHelper
# Create your models here.


class Vendor(TrackObjectStateMixin):
    id = None
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True)
    bio = models.TextField(null=True, blank=True)
    profile_img_url = models.ImageField(upload_to='vendors/profile_images/', null=True)
    identity = models.FileField(upload_to='vendors/identities/', null=True)
    themes = models.ManyToManyField('Theme')

    class Meta:
        ordering = ["last_updated"]
        
    @classmethod 
    def populate_file_fields(cls) -> tuple:
        file_tuple = tuple(f.name for f in cls._meta.get_fields() \
                            if isinstance(cls._meta.get_field(f.name), models.FileField)
                            )
        return file_tuple
     
    def populate_image_files(self) -> list:
        image_files = list(getattr(self, '{}'.format(f.name)) for f in self._meta.get_fields() \
                            if isinstance(self._meta.get_field(f.name), models.ImageField)
                            )
        return image_files
    
    def save(self, *args, **kwargs):
        """Optimize Compressing Images and Deletes former files when making an update
        """
        # former = get_old_object(Vendor, self.user)
        former = Vendor.objects.filter(pk=self.user)
        if former.exists():
            UserRelatedHelper(former.first()).remove_duplicate(self.populate_file_fields(), self)
                    
        return super().save(*args, **kwargs)
    
    
    def __str__(self) -> str:
        return self.user.first_name
    

class Store(TrackObjectStateMixin):
    owner = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='store', db_index=True)
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='vendors/stores/logo/', blank=True, null=True)
    description = models.CharField(max_length=250)
    
    
    
    @classmethod 
    def populate_file_fields(cls) -> tuple:
        file_tuple = tuple(f.name for f in cls._meta.get_fields() \
                            if isinstance(cls._meta.get_field(f.name), models.FileField)
                            )
        return file_tuple
     
    def populate_image_files(self) -> list:
        image_files = list(getattr(self, '{}'.format(f.name)) for f in self._meta.get_fields() \
                            if isinstance(self._meta.get_field(f.name), models.ImageField)
                            )
        return image_files
    
    def save(self, *args, **kwargs):
        """Optimize Compressing Images and Deletes former files when making an update
        """ 
        # remove duplicate files on update
        former = Store.objects.filter(pk=self.pk)
        if former.exists():
            UserRelatedHelper(former.first()).remove_duplicate(self.populate_file_fields(), self)
                    
        super().save(*args, **kwargs)
        
    def __str__(self) -> str:
        return self.name 


class Theme(TrackObjectStateMixin):
    name = models.CharField(max_length=20, unique=True)
    primary_color = models.CharField(max_length=7)
    secondary_color = models.CharField(max_length=7)
    background_color = models.CharField(max_length=7)
    text_color = models.CharField(max_length=7)
    link_color = models.CharField(max_length=7)
    button_color = models.CharField(max_length=7)
    
    def __str__(self) -> str:
        return self.name
    
    
class StoreSetting(TrackObjectStateMixin):
    """All custom settings associated to a store. vendors will 
       be able to customize ans style their store how they like. 
    """
    id = None  
    store = models.OneToOneField(Store, on_delete=models.CASCADE, primary_key=True, related_name='store_settings')
    use_theme = models.BooleanField(default=False)
    theme = models.CharField(max_length=200, null=True, blank=True)
    primary_color = models.CharField(max_length=7, blank=True, null=True)
    secondary_color = models.CharField(max_length=7, blank=True, null=True)
    background_color = models.CharField(max_length=7, blank=True, null=True)
    text_color = models.CharField(max_length=7, blank=True, null=True)
    link_color = models.CharField(max_length=7, blank=True, null=True)
    button_color = models.CharField(max_length=7, blank=True, null=True)
    banner_image = models.ImageField(upload_to='vendors/', blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    social_media = models.JSONField(default=dict, null=True)
    
    def __str__(self) -> str:
        return f"settings for {self.store.name}"
    
    
