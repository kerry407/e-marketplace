from rest_framework import serializers 
from .models import Vendor 


class VendorSerializer(serializers.ModelSerializer):
    profile_img_url = serializers.ImageField(required=False)
    
    class Meta:
        model = Vendor 
        exclude = ('user',)