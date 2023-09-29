from rest_framework import serializers # type: ignore
from django.contrib.auth import get_user_model # type: ignore
from datetime import datetime
from typing import Dict, Any
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = get_user_model() 
        fields = ["id", "first_name", "last_name", "email", "gender", "password", "password2"]
        extra_kwargs = {
            "password": {"write_only": True}
        }
        
    def validate(self, attrs: Dict[str, str]) -> Dict[str, Any]:
        
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("The two passwords do not match !")
        # Remove password2 as it is not part of model fields
        attrs.pop("password2")
        return attrs 
        
    def create(self, validated_data: Dict[str, Any]):
        email = validated_data["email"]
        confirm_account = get_user_model().objects.filter(email=email)
        
        # Check if we have a user with the entered email address
        if confirm_account.exists():
            raise serializers.ValidationError("An account already exists with this email")
        # If not, then create the user with the email and the rest of the validated data
        new_account = get_user_model().objects.create_user(**validated_data)
        return new_account
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs: Dict[str, str]) -> Dict[str, Any]:
        data = super().validate(attrs)
        if not self.user.is_verified and self.user.is_active:
            raise serializers.ValidationError(
                                                {
                                                 'detail': 'The email of this user must be verified to perform any action'
                                                }
                                             )
        now = datetime.now()
        refresh: str = self.get_token(self.user)
        data["access_token_lifetime"] = refresh.access_token.lifetime
        access_token_expiry = now + refresh.access_token.lifetime
        data["access_token_expiry"] = access_token_expiry.strftime("%Y-%m-%d %H:%M:%S")
        
        data.update(
            {
                "id": self.user.id,
                "email": self.user.email,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "gender": self.user.gender,
                "is_vendor": self.user.is_vendor,
                "is_superuser": self.user.is_superuser,
                "is_staff": self.user.is_staff,
            }
        )
        return data 
    
    
class ChangePasswordSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    
    
    

        
        
    



    
    