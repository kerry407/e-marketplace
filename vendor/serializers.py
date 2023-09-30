from rest_framework import serializers 
from .models import Vendor, Store 


class VendorSerializer(serializers.ModelSerializer):
    profile_img_url = serializers.ImageField(required=False)
    identity = serializers.FileField(required=False) 
    # user = serializers.StringRelatedField()
    is_vendor = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.pk
    
    def get_is_vendor(self, obj):
        return obj.user.is_vendor
    class Meta:
        model = Vendor 
        fields = '__all__'
        
        
class StoreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Store  
        exclude = ('owner',)