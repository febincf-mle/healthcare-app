from django.db import models
from accounts.models import Profile


class Doctor(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    qualification = models.CharField(max_length=255)
    years_of_experience = models.PositiveIntegerField()
    license_number = models.CharField(max_length=50, unique=True)

    def delete(self, *args, **kwargs):
        # Delete the related Profile instance first
        if self.profile:
            self.profile.delete()
        # Call the default delete method to delete the Patient instance
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Dr. {self.profile.first_name} {self.profile.last_name}"