# from django.db import models
from djongo import models as models
from account.models import User
from django.utils import timezone
from mapbox_location_field.models import LocationField
from dashboard.forms import CustomDictField, CustomListField
import time

# Create your models here.

class EventCategories(models.Model):
    id = models.ObjectIdField(db_column="_id")
    category_name = models.CharField(unique=True, max_length=255, db_column="_category_name")
    category_code = models.CharField(unique=True, max_length=255, db_column="_category_code")
    category_image_url = models.CharField(max_length=1000, db_column="_category_image_url")
    category_priority = models.PositiveIntegerField(unique=True, db_column="_category_priority")
    created_user = models.ForeignKey(User, related_name='created_user', on_delete=models.CASCADE, db_column="_created_user_id")
    updated_user = models.ForeignKey(User, related_name='updated_user', on_delete=models.CASCADE, db_column="_updated_user_id")
    created_date = models.FloatField(default=int(time.time()), db_column="_created_date")
    updated_date = models.FloatField(default=int(time.time()), db_column="_updated_date")
    status = models.PositiveIntegerField(db_column="_status")

    class Meta:
        verbose_name_plural = 'EventCategories'
        db_table = "tb1_event_categories"

    def __str__(self):
        return self.category_name

class Event(models.Model):
    id = models.ObjectIdField(db_column="_id")
    event_category = models.ForeignKey(EventCategories, related_name='event_category_name', on_delete=models.CASCADE, db_column='_event_category_id')
    event_name = models.CharField(max_length=255, unique=True, db_column="_event_name")
    event_uid = models.PositiveIntegerField(db_column='_event_uid')
    event_description = models.TextField(db_column='_event_description')
    event_scheduled_status = models.PositiveIntegerField(db_column='_event_scheduled_status')
    event_venue = models.CharField(max_length=255, unique=True, db_column='_event_venue')
    event_agenda = CustomListField(blank=True, default={}, null=True, db_column='_event_agenda')
    event_start_date = models.FloatField(blank=True, db_column='_event_start_date')
    event_end_date = models.FloatField(blank=True, db_column='_event_end_date')
    event_location = CustomDictField(blank=True, default={}, null=True, db_column='_event_location')
    event_points = models.PositiveIntegerField(db_column='_event_points')
    event_maximum_attende = models.PositiveIntegerField(db_column='_event_maximum_attende')
    created_user = models.ForeignKey(User, related_name='created_user_event', on_delete=models.CASCADE, db_column='_created_user_id')
    updated_user = models.ForeignKey(User, related_name='updated_user_event', on_delete=models.CASCADE, db_column='_updated_user_id')
    updated_date = models.FloatField(default=int(time.time()), db_column='_updated_date')
    created_date = models.FloatField(default=int(time.time()), db_column='_created_date')
    status = models.PositiveIntegerField(db_column='_status')

    class Meta:
        db_table = "tb1_events"

    def __str__(self):
        return self.event_name



class EventImage(models.Model):
    id = models.ObjectIdField(db_column='_id')
    event = models.ForeignKey(Event, related_name='event_image_event', on_delete=models.CASCADE, db_column='_event_id')
    image_url = models.CharField(max_length=1000, db_column='_image_url')
    image_position = models.PositiveIntegerField(db_column='_image_position')
    created_user = models.ForeignKey(User, related_name='created_user_event_image', on_delete=models.CASCADE, db_column='_created_user_id')
    updated_user = models.ForeignKey(User, related_name='updated_user_event_image', on_delete=models.CASCADE, db_column='_updated_user_id')
    created_date = models.FloatField(default=int(time.time()), db_column='_created_date')
    updated_date = models.FloatField(default=int(time.time()), db_column='_updated_date')
    status = models.PositiveIntegerField(db_column='_status')

    class Meta:
        db_table = "tb1_event_images"

    def __str__(self):
        return self.image_url


class Location(models.Model):
    location = LocationField(map_attrs={"center": [17.031645, 51.106715], "marker_color": "blue", "zoom": 2, "cursor_style": "pointer", "readonly": True})
