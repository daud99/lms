from django.urls import path
from dashboard import views

# TEMPLATE_TAGGING
app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name="index"),
]