from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager

class UserRole(models.Model):
    role_name = models.CharField(max_length=255, unique=True)
    role_type = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    status = models.PositiveIntegerField()

    def __str__(self):
        return self.role_name


class User(AbstractBaseUser, PermissionsMixin):

    username = None
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # additional fields

    full_name = models.CharField(max_length=255)
    job_category_id = models.CharField(max_length=255, default='1')
    organization_id = models.CharField(max_length=255, default='1')
    image_url = models.CharField(max_length=1000)
    fcm_id = models.PositiveIntegerField()
    os_type = models.PositiveIntegerField()
    device_unique_id = models.PositiveIntegerField()
    notification_status = models.PositiveIntegerField()
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    status = models.PositiveIntegerField()
    role = models.ForeignKey(UserRole, related_name="user_role_related_name", on_delete=models.CASCADE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email