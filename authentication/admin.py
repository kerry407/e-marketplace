from django.contrib import admin

# Register your models here.
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email','first_name', 'last_name', 'is_active', 'is_verified',)
    list_filter = ('email', 'is_staff', 'is_active', 'is_verified', )
    search_fields = ('email',)
    ordering = ('email',)
    


    
