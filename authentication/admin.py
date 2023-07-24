from django.contrib import admin

# Register your models here.
from .models import CustomUser, Vendor

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email','first_name', 'last_name', 'is_active', 'is_verified', 'created_at')
    list_filter = ('email', 'is_staff', 'is_active', 'is_verified', 'created_at')
    search_fields = ('email',)
    ordering = ('email',)
    

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'bio', 'profile_img', 'identity')
    list_filter = ('user',)
    search_fields = ('user',)
    
