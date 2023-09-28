from rest_framework import serializers 
from .models import Vendor 


class VendorSerializer(serializers.ModelSerializer):
    profile_img_url = serializers.ImageField(required=False)
    identity = serializers.ImageField(required=True) 
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Vendor 
        fields = '__all__'