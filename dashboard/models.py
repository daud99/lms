from django.db import models
from djongo import models as djongo_models
from dashboard.forms import CustomListField, CustomDictField
# Create your models here.


class College(djongo_models.Model):
    _id = djongo_models.ObjectIdField()
    name = djongo_models.CharField(max_length=255)
    objects = djongo_models.DjongoManager()

class Student(djongo_models.Model):
    _id = djongo_models.ObjectIdField()
    name = djongo_models.CharField(max_length=155)
    courses = CustomDictField(blank=True, default={}, null=True)
    college = djongo_models.ForeignKey(College, on_delete=djongo_models.CASCADE)
    object = djongo_models.DjongoManager()


