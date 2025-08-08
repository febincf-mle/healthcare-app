from django.urls import path
from .views import (
    PatientDoctorMappingListCreateAPIView,
    PatientDoctorMappingByPatientAPIView,
    PatientDoctorMappingDeleteAPIView
)

urlpatterns = [
    path('api/mappings/', PatientDoctorMappingListCreateAPIView.as_view(), name='mapping-list-create'),
    path('api/mappings/<int:patient_id>/', PatientDoctorMappingByPatientAPIView.as_view(), name='mapping-by-patient'),
    path('api/mappings/<int:pk>/delete/', PatientDoctorMappingDeleteAPIView.as_view(), name='mapping-delete'),
]
