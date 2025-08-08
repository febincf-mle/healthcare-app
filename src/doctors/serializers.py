from rest_framework import serializers
from accounts.models import Profile
from accounts.serializers import ProfileSerializer
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = Doctor
        fields = [
            "id", "profile", "specialization", "qualification",
            "years_of_experience", "license_number"
        ]
        read_only_fields = ["id"]

    
    def create(self, validated_data):

        request_user = self.context.get("request").user
        profile_data = validated_data.pop("profile")

        profile = Profile.objects.create(
            created_by=request_user, 
            **profile_data
        )

        return Doctor.objects.create(
            profile=profile,
            **validated_data
        )

    def update(self, instance, validated_data):

        profile_data = validated_data.pop("profile", None)

        if profile_data:
            # Cannot change the created_by field,
            # of the profile.
            profile_data.pop("created_by", None)
            for key, val in profile_data.items():
                setattr(instance.profile, key, val)
            instance.profile.save()
        
        # Update doctor-specific fields.
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance