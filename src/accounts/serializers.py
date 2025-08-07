from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(
        min_length=8, 
        allow_blank=False, 
        write_only=True
        )
    
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token

    def validate(self, attrs):
        # Replace 'username' with 'email'
        attrs['username'] = attrs.get('email')
        return super().validate(attrs)
    