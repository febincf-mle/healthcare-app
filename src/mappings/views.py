from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from doctors.models import Doctor
from doctors.serializers import DoctorSerializer
from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingSerializer, PatientDoctorMappingReadSerializer


class PatientDoctorMappingListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Retrieve all patient-doctor mappings."""
        mappings = (
            PatientDoctorMapping.objects
            .select_related(
                'patient', 
                'patient__profile',  
                'doctor', 
                'doctor__profile'    
            )
        )
        serializer = PatientDoctorMappingReadSerializer(mappings, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Assign a doctor to a patient."""
        serializer = PatientDoctorMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientDoctorMappingByPatientAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, patient_id):
        """Get all doctors assigned to a specific patient."""
        doctors = Doctor.objects.filter(
            patient_mappings__patient_id=patient_id
        ).select_related('profile')
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)


class PatientDoctorMappingDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        """Remove a doctor from a patient."""
        mapping = get_object_or_404(PatientDoctorMapping, pk=pk)
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)