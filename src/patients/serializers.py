from rest_framework import serializers
from accounts.models import Profile
from accounts.serializers import ProfileSerializer
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = Patient
        fields = [
            "id", "profile", "blood_group", "height_cm", "weight_kg",
            "emergency_contact_name", "emergency_contact_phone",
            "medical_history", "current_medications"
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        profile_data = validated_data.pop("profile")
        request_user = self.context["request"].user

        profile = Profile.objects.create(
            created_by=request_user,
            **profile_data
        )
        patient = Patient.objects.create(profile=profile, **validated_data)
        return patient

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", None)

        # Update profile if provided
        if profile_data:
            for attr, value in profile_data.items():
                setattr(instance.profile, attr, value)
            instance.profile.save()

        # Update patient-specific fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance