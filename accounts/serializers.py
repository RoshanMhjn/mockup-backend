from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer, JWTSerializer, LoginSerializer
from .models import User

class CustomRegisterSerializer(RegisterSerializer):
  first_name = serializers.CharField(required=True,max_length=30)
  last_name = serializers.CharField(required=True, max_length=30)
  phone_number = serializers.CharField(required=False, max_length=20)
  
  def get_cleaned_data(self):
    data = super().get_cleaned_data()
    data.update({
      'first_name': self.validated_data.get('first_name', ''),
      'last_name': self.validated_data.get('last_name', ''),
      'phone_number': self.validated_data.get('phone_number', ''),
    })
    return data
  
  def save(self,request):
    user = super().save(request)
    user.first_name = self.cleaned_data.get('first_name')
    user.last_name = self.cleaned_data.get('last_name')
    user.phone_number = self.cleaned_data.get('phone_number')
    
    user.save()
    
    return user

class CustomUserDetailsSerializer(UserDetailsSerializer):
  
  class Meta:
    model = User
    fields = [
      'id', 'email', 'username', 'first_name', 'last_name', 'phone_number', 'email_verified', 'created_at', 'updated_at',
    ]
    read_only_fields = ['id', 'email', 'email_verified', 'created_at', 'updated_at']

class CustomJWTSerializer(JWTSerializer):
    user = CustomUserDetailsSerializer(read_only=True)

class CustomLoginSerializer(LoginSerializer):
    """Custom login serializer that includes user details in response"""
    pass

class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name', 'full_name','phone_number', 'email_verified',
            'created_at', 'updated_at','is_staff', 'is_superuser',
        ]
        read_only_fields = [
            'id', 'email', 'email_verified', 'created_at', 'updated_at','is_staff', 'is_superuser',
        ]

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    
    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New passwords don't match.")
        return data
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value