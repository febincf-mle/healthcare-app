from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager


AUTH_USER_MODEL = settings.AUTH_USER_MODEL

class Gender(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'
    OTHER = 'O', 'Other'


class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    age = models.PositiveIntegerField(default=30)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        default=Gender.OTHER
    )
    date_of_birth = models.DateField()
    address = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )


class CustomUser(AbstractBaseUser, PermissionsMixin):

    name = models.CharField(max_length=200)
    email = models.EmailField(_('email address'), unique=True)
    age = models.PositiveIntegerField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email