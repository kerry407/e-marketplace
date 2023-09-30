from django.contrib import admin
from .models import Vendor, Store, StoreSetting
# Register your models here.

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'bio', 'profile_img_url', 'identity')
    list_filter = ('user',)
    search_fields = ('user',)
    

@admin.register(Store) 
class StoreAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'created_at', 'last_updated')
    list_filter = ('owner', 'last_updated')
    
    
@admin.register(StoreSetting) 
class StoreSettingsAdmin(admin.ModelAdmin):
    list_display = ('store', 'created_at', 'last_updated')
    list_filter = ('store', 'last_updated')