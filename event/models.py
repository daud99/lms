from django.db import models
from account.models import User
from django.utils import timezone
from jsonfield import JSONField


# Create your models here.

class EventCategories(models.Model):
    class Meta:
        verbose_name_plural = 'EventCategories'
    category_name = models.CharField(unique=True, max_length=255)
    category_code = models.CharField(unique=True, max_length=255)
    category_image_url = models.CharField(unique=True, max_length=1000)
    category_priority = models.PositiveIntegerField(unique=True)
    created_user = models.ForeignKey(User, related_name='created_user', on_delete=models.CASCADE)
    updated_user = models.ForeignKey(User, related_name='updated_user', on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    status = models.PositiveIntegerField()

    def __str__(self):
        return self.category_name

class Event(models.Model):
    event_category = models.ForeignKey(EventCategories, related_name='event_category_name', on_delete=models.CASCADE)
    event_name = models.CharField(max_length=255, unique=True)
    event_uid = models.PositiveIntegerField()
    event_description = models.TextField()
    event_scheduled_status = models.PositiveIntegerField()
    event_venue = models.CharField(max_length=255, unique=True)
    event_agenda = JSONField(blank=True, default={})
    event_start_date = models.DateTimeField(blank=True)
    event_end_date = models.DateTimeField(blank=True)
    event_location = JSONField(blank=True, default={})
    event_points = models.PositiveIntegerField()
    event_maximum_attende = models.PositiveIntegerField()
    created_user = models.ForeignKey(User, related_name='created_user_event', on_delete=models.CASCADE)
    updated_user = models.ForeignKey(User, related_name='updated_user_event', on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    status = models.PositiveIntegerField()

    def __str__(self):
        return self.event_name



class EventImage(models.Model):
    event = models.ForeignKey(Event, related_name='event_image_event', on_delete=models.CASCADE)
    image_url = models.CharField(max_length=1000)
    image_position = models.PositiveIntegerField()
    created_user = models.ForeignKey(User, related_name='created_user_event_image', on_delete=models.CASCADE)
    updated_user = models.ForeignKey(User, related_name='updated_user_event_image', on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    status = models.PositiveIntegerField()

    def __str__(self):
        return self.image_url

