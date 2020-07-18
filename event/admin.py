from django.contrib import admin
from .models import EventCategories, Event, EventImage

# Register your models here.

admin.site.register(EventCategories)
admin.site.register(Event)
admin.site.register(EventImage)