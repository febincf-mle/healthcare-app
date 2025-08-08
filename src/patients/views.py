import logging
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.exceptions import ValidationError
from .models import Patient
from .serializers import PatientSerializer
from .pagination import PatientPagination


logger = logging.getLogger(__name__)

class PatientListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Retrieve all patients created by the authenticated user (with pagination)."""
        patients = (Patient
                    .objects
                    .filter(profile__created_by=request.user)
                    .prefetch_related('profile')
                    .order_by('-id'))
        paginator = PatientPagination()
        page = paginator.paginate_queryset(patients, request)
        serializer = PatientSerializer(page, many=True)
        logger.info(f"User {request.user} retrieved patient list.")
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """Create a new patient."""
        serializer = PatientSerializer(data=request.data, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
            patient = serializer.save()
            logger.info(f"User {request.user} created patient {patient.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            logger.warning(f"Validation error while creating patient by user {request.user}: {e}")
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error while creating patient: {e}", exc_info=True)
            return Response({"error": "Something went wrong."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PatientDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(Patient, pk=pk, profile__created_by=user)

    def get(self, request, pk):
        """Get details of a specific patient."""
        patient = self.get_object(pk, request.user)
        serializer = PatientSerializer(patient)
        logger.info(f"User {request.user} retrieved patient {pk}")
        return Response(serializer.data)

    def put(self, request, pk):
        """Update patient details."""
        patient = self.get_object(pk, request.user)
        serializer = PatientSerializer(patient, data=request.data, partial=True, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info(f"User {request.user} updated patient {pk}")
            return Response(serializer.data)
        except ValidationError as e:
            logger.warning(f"Validation error while updating patient {pk} by user {request.user}: {e}")
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error while updating patient {pk}: {e}", exc_info=True)
            return Response({"error": "Something went wrong."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        """Delete a patient record."""
        patient = self.get_object(pk, request.user)
        patient.delete()
        logger.info(f"User {request.user} deleted patient {pk}")
        return Response({"message": "Patient deleted successfully."}, status=status.HTTP_204_NO_CONTENT)