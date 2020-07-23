from django.urls import path
from dashboard import views
from event import views as event_views
# TEMPLATE_TAGGING
app_name = 'dashboard'

urlpatterns = [
    path('', event_views.listEvent, name="index"),
    path('events', event_views.listEvent, name="events"),
    path('event/id/<str:id>', event_views.detailEvent, name="event_detail"),
    path('event/add', event_views.addEvent, name="add_event"),
    path('event/delete/id/<str:id>', event_views.deleteEvent, name="delete_event"),
    path('event/edit/id/<str:id>', event_views.editEvent, name="edit_event"),
    path('event/add/category', event_views.addEventCategory, name="add_event_category"),
    path('event/edit/category/<str:id>', event_views.editEventCategory, name="edit_event_category"),
    path('event/delete/category/<str:id>', event_views.deleteEventCategory, name="delete_event_category"),
    path('event/categories', event_views.listEventCategories, name="event_categories"),
]

