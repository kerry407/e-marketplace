from rest_framework import permissions  

class IsOwnerOrReadOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        
        # Allow full access to only verified users.
        if request.user.is_verified:
            return True 
        return False 
    
    def has_object_permission(self, request, view, obj):
        # Allow Read-Only access to all users
        if request.method in permissions.SAFE_METHODS:
            return True 
        
        # Allow full access to admin users.
        if request.user.is_staff:
            return True 
        
        # Check if the object has a 'user' attribute, then return the truthiness.
        if hasattr(obj, 'user'):
            return obj.user == request.user 