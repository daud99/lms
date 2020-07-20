from django.urls import path
from dashboard import views
from event import views as event_views
# TEMPLATE_TAGGING
app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name="index"),
    path('event/add', event_views.addEvent, name="add_event"),
    path('event/add/category', event_views.addEventCategory, name="add_event_category"),
    path('event/edit/category/<int:id>', event_views.editEventCategory, name="edit_event_category"),
    path('event/delete/category/<int:id>', event_views.deleteEventCategory, name="delete_event_category"),
    path('event/categories', event_views.listEventCategories, name="event_categories"),
]