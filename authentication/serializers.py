from rest_framework import serializers # type: ignore
from django.contrib.auth import get_user_model # type: ignore
from typing import Dict, Any

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    
    class Meta:
        model = get_user_model() 
        fields = ["id", "first_name", "last_name", "email", "gender", "password", "password2"]
        extra_kwargs = {
            "password": {"write_only": True}
        }
        
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        
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
    
    