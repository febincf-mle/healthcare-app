from django.urls import path
from .views import PatientListCreateAPIView, PatientDetailAPIView


urlpatterns = [
    path('', PatientListCreateAPIView.as_view(), name='patient-list-create'),
    path('<int:pk>/', PatientDetailAPIView.as_view(), name='patient-detail'),
]