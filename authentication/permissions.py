from rest_framework import permissions 

class CustomUserPermissions(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.user.is_verified:
            return True 
        return False 