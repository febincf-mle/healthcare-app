from django.urls import path
from .views import (
    PatientDoctorMappingListCreateAPIView,
    PatientDoctorMappingByPatientAPIView,
)

urlpatterns = [
    path('', PatientDoctorMappingListCreateAPIView.as_view(), name='mapping-list-create'),
    path('<int:pk>/', PatientDoctorMappingByPatientAPIView.as_view(), name='mapping-by-patient'),
]