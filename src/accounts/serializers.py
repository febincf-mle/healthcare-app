from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Profile


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
    

class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[])
    phone_number = serializers.CharField(validators=[])

    class Meta:
        model = Profile
        fields = [
            "first_name", "last_name", "email", "phone_number",
            "gender", "age", "date_of_birth", "address"
        ]
    
    def validate_email(self, value):
        if self.instance and self.instance.email == value:
            print(self.instance, "This is the self.instance you wanted bitch")
            return value

        if Profile.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_phone_number(self, value):
        if self.instance and self.instance.phone_number == value:
            return value

        if Profile.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already in use.")
        return value
    

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