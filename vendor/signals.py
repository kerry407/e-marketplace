from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Vendor, Store, StoreSetting

@receiver(post_save, sender=Vendor)
def update_user_instance(sender, instance, created, **kwargs) -> None:
    if created:
        user = instance.user
        user.is_vendor = True 
        user.save()
        
        
@receiver(post_save, sender=Store)
def generate_store_settings_on_create(sender, instance, created, **kwargs):
    if created:
        StoreSetting.objects.create(store=instance)