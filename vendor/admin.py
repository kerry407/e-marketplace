from django.contrib import admin
from .models import Vendor 
# Register your models here.

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'bio', 'profile_img_url', 'identity')
    list_filter = ('user',)
    search_fields = ('user',)