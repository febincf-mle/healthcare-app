import logging
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import Doctor
from .serializers import DoctorSerializer


logger = logging.getLogger(__name__)

class DoctorListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve all doctors created by the authenticated user (with pagination)."""
        doctors = (
            Doctor
            .objects
            .all()
            .select_related('profile')
            .order_by("-id")
        )
        serializer = DoctorSerializer(doctors, many=True)
        logger.info(f"User {request.user} retrieved doctors list.")
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """Create a new Doctor. The User has to be authenticated for creation"""
        serializer = DoctorSerializer(data=request.data, context={ 'request': request })
        try:
            serializer.is_valid(raise_exception=True)
            doctor = serializer.save()
            logger.info(f"User {request.user} created doctor {doctor.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            logger.warning(f"Validation error while creating doctor by user {request.user}: {e}")
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            logger.warning(f"Integrity error while creating doctor by user {request.user}: {e}")
            return Response({"error": 'Email or Phonenumber already exists'}, status=status.HTTP_400_BAD_REQUEST)    
        except Exception as e:
            logger.error(f"Unexpected error while creating doctor: {e}", exc_info=True)
            return Response({"error": "Something went wrong."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DoctorDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        queryset = (
            Doctor.objects
            .select_related('profile') 
        )
        return get_object_or_404(queryset, pk=pk, profile__created_by=user)
    
    def get(self, request, pk):
        """Get details of a specific Doctor"""
        doctor = self.get_object(pk, request.user)
        serializer = DoctorSerializer(doctor)
        logger.info(f"User {request.user} retrieved doctor {pk}")
        return Response(serializer.data)

    def put(self, request, pk):
        """Update the doctor details"""
        instance = self.get_object(pk, request.user)
        serializer = DoctorSerializer(
            instance,
            data=request.data,
            partial=True,
            context = { 'request': request }
        )

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info(f"User {request.user} updated doctor {pk}")
            return Response(serializer.data)
        except ValidationError as e:
            logger.warning(f"Validation error while updating doctor {pk} by user {request.user}: {e}")
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error while updating doctor {pk}: {e}", exc_info=True)
            return Response({"error": "Something went wrong."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def delete(self, request, pk):
        """Delete specific doctor details"""
        doctor = self.get_object(pk, request.user)
        doctor.delete()
        logger.info(f"User {request.user} deleted doctor {pk}")
        return Response({"message": "Doctor deleted successfully."}, status=status.HTTP_204_NO_CONTENT)