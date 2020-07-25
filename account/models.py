from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from djongo import models as djongo_models
from dashboard.forms import CustomDictField
import time


from .managers import CustomUserManager

class UserRole(djongo_models.Model):
    id = djongo_models.ObjectIdField(db_column='_id')
    role_name = djongo_models.CharField(max_length=255, unique=True, db_column='_user_role_name')
    role_type = djongo_models.PositiveIntegerField(default=0, db_column='_user_role_type')
    created_date = djongo_models.FloatField(default=int(time.time()), db_column='_created_date')
    updated_date = djongo_models.FloatField(default=int(time.time()), db_column='_updated_date')
    status = djongo_models.PositiveIntegerField(db_column='_status')


    class Meta:
        db_table = "tb1_user_roles"


    def __str__(self):
        return self.role_name


class User(AbstractBaseUser, PermissionsMixin):
    id = djongo_models.ObjectIdField(db_column="_id")
    username = None
    email = models.EmailField(_('email address'), unique=True, db_column="_user_email")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # additional fields

    full_name = models.CharField(max_length=255, db_column="_user_full_name")
    user_password = models.CharField(max_length=255, db_column="_user_password")
    job_category_id = models.CharField(max_length=255, default='1', db_column="_user_job_category_id")
    organization_id = models.CharField(max_length=255, default='1', db_column="_organization_id")
    image_url = models.CharField(max_length=1000, blank=True, db_column="_user_image")
    fcm_id = models.PositiveIntegerField(blank=True, db_column="_user_fcm_id")
    os_type = models.PositiveIntegerField(blank=True, db_column="_user_os_type")
    device_unique_id = models.PositiveIntegerField(blank=True, db_column="_user_device_unique_id")
    notification_status = models.PositiveIntegerField(blank=True, db_column="_user_noitfication_status")
    location = CustomDictField(blank=True, default={}, null=True, db_column="_location")
    created_date = models.FloatField(default=int(time.time()), db_column="_created_date")
    updated_date = models.FloatField(default=int(time.time()), db_column="_update_date")
    status = models.PositiveIntegerField(blank=True, db_column="_status")
    role = models.ForeignKey(UserRole, related_name="user_role_related_name", on_delete=models.CASCADE, db_column="_user_role_id")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = "tb1_users"

    def __str__(self):
        return self.email
