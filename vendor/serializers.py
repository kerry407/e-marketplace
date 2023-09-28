from rest_framework import serializers 
from .models import Vendor 


class VendorSerializer(serializers.ModelSerializer):
    profile_img_url = serializers.ImageField(required=False)
    identity = serializers.FileField(required=False) 
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Vendor 
        fields = '__all__'