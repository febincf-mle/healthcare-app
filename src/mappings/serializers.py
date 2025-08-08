from rest_framework import serializers
from patients.serializers import PatientSerializer
from doctors.serializers import DoctorSerializer
from .models import PatientDoctorMapping    


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctorMapping
        fields = ['id', 'patient', 'doctor', 'assigned_at']
        read_only_fields = ['id', 'assigned_at']


class PatientDoctorMappingReadSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    doctor = DoctorSerializer()

    class Meta:
        model = PatientDoctorMapping
        fields = ['id', 'patient', 'doctor', 'assigned_at']
        read_only_fields = "__all__"
